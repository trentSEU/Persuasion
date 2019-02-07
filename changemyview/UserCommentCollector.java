package com.github.jreddit.changemyview;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;











import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

import com.github.jreddit.entity.Comment;
import com.github.jreddit.entity.Submission;
import com.github.jreddit.exception.RetrievalFailedException;
import com.github.jreddit.retrieval.Comments;
import com.github.jreddit.retrieval.Submissions;
import com.github.jreddit.retrieval.params.CommentSort;
import com.github.jreddit.retrieval.params.UserOverviewSort;

public class UserCommentCollector extends Database {

	private static String tableName = "user_comments";

	public UserCommentCollector(String databaseName, String userName,
			String password) {
		super(databaseName, userName, password);
	}

	public UserCommentCollector(String databaseName) {
		super(databaseName);
	}

	public UserCommentCollector() throws IOException, ParseException {
		super();
	}

	/**
	 * Gets a comment entity and checks if it exists in the database
	 * If it does, adds it to the database
	 * If not, updates the record if any changes have happened
	 * @param comment
	 * @throws SQLException
	 */
	public void addOrUpdateComment(Comment comment) throws SQLException {
		String id = comment.getIdentifier();
		if (count(tableName, "CID", id) == 0) // if the comment does not exist
		{
			System.out.println("Adding the new comment...");
			addComment(comment);
		} else // if submission already exists
		{
			System.out.println("the comment already exists!");
			updateComment(comment);
		}
	}

	/**
	 * adds a new comment
	 * @param comment
	 * @throws SQLException
	 */
	public void addComment(Comment comment) throws SQLException {
		String commentId = comment.getIdentifier();
		String submissionId = comment.getParentId();
		String author = comment.getAuthor();
		String text = comment.getBody();
		String parentSubmissionId=comment.getLinkId();
		int score = comment.getScore();

		Double created = comment.getCreated();
		String sql = "INSERT INTO "
				+ tableName
				+ " (CID, ParentId, ParentSubmissionId, Author, Text, Score, Created) "
				+ "VALUES ('" + commentId + "','" + submissionId + "','"
				+ parentSubmissionId+"','"
				+ author + "','"
				+ text.replaceAll("\'", "\'\'").replaceAll("\\\\", "")
				+ "','" + score + "','"
				+ created + "')";

		Statement stmt = connection.createStatement();
		stmt.executeUpdate(sql);
	}// end of add function
	/**
	 * Update comment info in user comments if any changes has happened
	 * only text and score can be checked directly from comments of user
	 * for other info such as replies, delta, explanation, etc., parent
	 * submission needs to be retrieved first
	 * @param comment
	 * @throws SQLException
	 */
	public static void updateComment(Comment comment) throws SQLException {
		// get the old record
		boolean textFlg, scoreFlg = false;
		String commentId = comment.getIdentifier();
		Statement stmt = connection.createStatement();
		String sql = "SELECT * FROM " + tableName + " WHERE CID='" + commentId
				+ "'";
		ResultSet rs = stmt.executeQuery(sql);
		if (rs.next()) {
			// new information from server
			String text = comment.getBody();
			int score = comment.getScore();
			// old information from database
			String oldText = rs.getString("Text");
			int oldScore = rs.getInt("Score");
			// compare information
			System.out.println("***changes:");
			textFlg = compareString("Text", oldText, text);
			scoreFlg = compareInt("Score", oldScore, score);
			if (textFlg || scoreFlg) {
				sql = "UPDATE " + tableName + " SET " + "Text='"
						+ text.replace("\'", "\'\'") + "', Score=" + score
						+ " WHERE CID='" + commentId + "'";
				stmt.executeUpdate(sql);
				System.out.println("Comment updated");
			}
		}// if for reading from database
	}

	/**
	 * Gets a comment entity and analyzes its comments to the depth of two to check if 
	 * the deltaBot has confirmed the delta point
	 * @param comment
	 * @return a JSON object with the delta information, its explanation, and the author who is awarding delta
	 * delta is 1 if awarded and 0 if not
	 */
	@SuppressWarnings("unchecked")
	public static JSONObject deltaBot(Comment comment) {
		JSONObject deltaObject = new JSONObject();
		deltaObject.put("explanation", "");
		deltaObject.put("author", "");
		deltaObject.put("deltaAwarded", 0);
		if (comment.hasRepliesSomewhere()) {
			List<Comment> levelTwoComments = comment.getReplies();
			for (Comment levelTwoComment : levelTwoComments) {
				if (levelTwoComment.hasRepliesSomewhere()) {
					List<Comment> levelThreeComments = levelTwoComment
							.getReplies();
					for (Comment levelThreeComment : levelThreeComments) {
						if (levelThreeComment.getAuthor().equals("DeltaBot")
								&& levelThreeComment.getBody().startsWith(
										"Confirmed")) {
							System.out.println("Delta is awarded");
							System.out.println("Text: " + comment.getBody());
							System.out.println("Explanation: "
									+ levelTwoComment.getBody());
							deltaObject.put("explanation",
									levelTwoComment.getBody());
							deltaObject.put("author",
									levelTwoComment.getAuthor());
							deltaObject.put("deltaAwarded", 1);
						}// if delta is awarded
					}// for level three comments
				}// if level two has replies
			}// for
		}// if level one has replies
		return deltaObject;
	}

	/**
	 * for all the users, retrieve comments and updates the table with linkParent
	 * @param restClient
	 * @param user
	 * @throws SQLException
	 */
	/*
	public void addLinkParent()
			throws SQLException {
		//UserCommentTable userCommentTable = new UserCommentTable("reddit_cmv");
		//userCommentTable.connect();
		// get all the users from the users' table
		connect();
		ResultSet users = returnAll("users");
		Comments cmnts = new Comments(restClient, user);
		int userIterations = 0;
		boolean flag = false;// false;
		while (users.next()) // users loop
		{
			try {
				System.out.println("--------------User " + ++userIterations);
				String userName = users.getString("UserName");
				 if(userName.equals("AlterdCarbon")) {flag=true;}
				if (flag) { // skip users
					System.out.println(userName);
					Comment after = null;
					// counts the total number of comments by a user
					int count = 0; 
					int commentIterations = 0;
					do // comments loop for each user
					{
						List<Comment> comments = cmnts.ofUser(userName,
								UserOverviewSort.NEW, null, count, 100, after,
								null, false);
						System.out.println(comments.size());
						// if no more comments are available the returned array
						// list is empty
						if (comments.size() == 0) {
							System.out
									.println("----No more comments available----");
							break;
						}
						for (int i = 0; i < comments.size(); i++) {
							System.out.println("----Comment " + (i + 1)
									+ "------Total: " + count);
							count = (commentIterations * 100) + (i + 1);
							Comment comment = comments.get(i);
							after = comment;
							//if the comment belongs to cmv
							if (comment.getSubredditId().equals("t5_2w2s8")) 
							{
								System.out.println("parent: "
										+ comment.getParentId());
								System.out.println("author: "
										+ comment.getAuthor());
								System.out.println("subrredit: "
										+ comment.getSubreddit());
								// find the comment and update the linkId
								Statement stm = connection.createStatement();
								String sql = "UPDATE user_comments SET parentSubmissionId='"
										+ comment.getLinkId()
										+ "' WHERE CID='"
										+ comment.getIdentifier()+"'";
								stm.executeUpdate(sql);
							}
						}
						++commentIterations;
					} while (true);
				}// end of flag
			}// end try
			catch (RetrievalFailedException e) {
				e.printStackTrace();
				continue;
			}
		}// end of while users
	}// -----end of function
	*/
	
	// Adds the comments if the comment is new, updates them if the comment
	// already exists
	/**
	 * Retrieves the user comment info for all the users in the user table
	 * adds or updates this information in user comments table
	 * @param restClient
	 * @param user
	 * @throws SQLException
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public void getUserComments(String sourceTable)
			throws SQLException, IOException, ParseException {
		// get all the users from the users' table
		connect();
		UserCollector userRecord = new UserCollector();
		ResultSet users = returnAll(sourceTable);
		Comments cmnts = new Comments(restClient, user);
		int userIterations = 0;
		boolean flag = false;
		while (users.next()) // users loop
		{
			//boolean flag = false;
			try {
				System.out.println("--------------User " + ++userIterations);
				String userName = users.getString("UserName");
				//to add conditions such as start from a specific userName
				//or only fetch comments with users with cmvComments==null
				//flag declaration needs to be moved accordingly
				//if (users.getObject("cmvComments")==null) {
				 if (users.getString("UserName").equals("Pinewood74")) {
					flag = true;
				}
				if (flag) { // skip users
					System.out.println(userName);
					Comment after = null;
					int count = 0; // counts the total number of comments by a user
					//int cmvComments = 0;
					int commentIterations = 0;
					do // comments loop for each user
					{
						List<Comment> comments = cmnts.ofUser(userName,
								UserOverviewSort.NEW, null, count, 100, after,
								null, false);
						System.out.println(comments.size());
						// if no more comments are available the returned array
						// list is empty
						if (comments.size() == 0) {
							System.out
									.println("----No more comments available----");
							break;
						}
						for (int i = 0; i < comments.size(); i++) {
							System.out.println("----Comment " + (i + 1)
									+ "------Total: " + count);
							count = (commentIterations * 100) + (i + 1);
							Comment comment = comments.get(i);
							/*System.out.println("Comment is provided in "
									+ comment.getSubreddit());*/
							after = comment;
							//if the comment belongs to cmv
							if (comment.getSubredditId().equals("t5_2w2s8")) 
							{
								System.out.println("parent: "
										+ comment.getLinkId());
								System.out.println("author: "
										+ comment.getAuthor());
								System.out.println("subrredit: "
										+ comment.getSubreddit());
								addOrUpdateComment(comment);
							}
						}
						++commentIterations;
					} while (true);
					// updating user info
					// updates user information with their total number of
					userRecord.updateUserTotalParticipation(userName, count);
					System.out.println("total comments by user: "+ count);
				}// end of flag
			}// end try
			catch (RetrievalFailedException e) {
				e.printStackTrace();
				continue;
			}
		}// end of while users		
	}// end of function
// ---------------------------------------------------------------------------------
/**
 * when accessing user_comment, not all of the attributes including delta information and 
 * number of replies, therefore, for every comment in user_comments, the parent submission 
 * is retrieved, along with its associated comments. The user comment is then searched in the
 * submission comment tree to extract the missing attributes
 * AuthorFlair in this table represents the authorFlair at the time of data collection
 * @throws Exception
 */
public void fillExtraAttributes() throws Exception
{
	connect();
	ResultSet userComments=returnAll(tableName);
	Boolean flag=false;
	while(userComments.next())
	{
		String commentID=userComments.getString("CID");
		if(commentID.equals("cqa414c"))
		{
			flag=true;
		}
		String parentID=userComments.getString("ParentSubmissionId").substring(3);
		Comment found=null;
		Comments cmnts = new Comments(restClient, user);
		List<Comment> comments;
		if(flag)
		{
			try
			{
				comments = cmnts.ofSubmission(parentID, null,-1, -1, 1000, CommentSort.NEW);
			}
			catch(com.github.jreddit.exception.RetrievalFailedException e)
			{
				System.out.println("***PARENT NOT FOUND");
				continue;
			}
			System.out.println("----------------------------------");
			System.out.println("finding comment for user "+userComments.getString("Author")+" with comment ID: "+commentID);
			for(Comment comment:comments)
			{
				found=findComment(comment,commentID);
				if(found!=null) break;
			}
			if(found==null)
			{
				//throw new Exception("comment should exist when retrieving parent");
				System.out.println("***COMMENT DID NOT EXIST");
				continue;
			}
			System.out.println("found: "+found);
			JSONObject delta=deltaBot(found);
			int authorFlair=found.getAuthorFlair();
			int numReplies=found.getReplies().size();
			int deltaAwarded=(Integer) delta.get("deltaAwarded");
			String deltaAwardedBy=(String) delta.get("author");
			String explanation=(String) delta.get("explanation");
			
			System.out.println("delta awarded: "+deltaAwarded);
			if(deltaAwarded==1) 
			{
				System.out.println("parent id: "+parentID);
				System.out.println(deltaAwardedBy);
				System.out.println(explanation);
			}
			//adding the new information to user_comments
			String sql = "UPDATE "
					+ tableName +
					" SET NumReplies='" + numReplies
					+ "', AuthorFlair='" + authorFlair 
					+ "', DeltaAwarded='" + deltaAwarded 
					+ "', DeltaAwardedBy='" + deltaAwardedBy
					+ "', Explanation='" + explanation.replace("\'", "\'\'") +
					"' WHERE CID='"+userComments.getString("CID")+"'";
			//System.out.println(sql);
			Statement stmt = connection.createStatement();
			stmt.executeUpdate(sql);
		}//end of if
	}
}
//----------------------------------------------------
/**
 * Given a comment tree, returns the comment object with the given ID
 * @param root
 * @param id
 * @return
 */
public Comment findComment(Comment root, String id)
{
	if(root.getFullName().substring(3).equals(id)) return root;
	for(int i=0;i<root.getReplies().size();i++)
	{
		Comment found=findComment(root.getReplies().get(i), id);
		if(found!=null) return found;
	}
	return null;
}
//---------------------------------------------------

}//end of class