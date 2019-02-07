package com.github.jreddit.changemyview;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

import com.github.jreddit.entity.Comment;
import com.github.jreddit.exception.RetrievalFailedException;
import com.github.jreddit.retrieval.Comments;
import com.github.jreddit.retrieval.params.CommentSort;

public class SubmissionCommentCollector extends Database {

	private static String tableName = "submission_comments";

	public SubmissionCommentCollector(String databaseName, String userName,
			String password) {
		super(databaseName, userName, password);
	}

	public SubmissionCommentCollector(String databaseName) {
		super(databaseName);
	}

	public SubmissionCommentCollector() throws IOException, ParseException {
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
		if (count(tableName, "CID", id) == 0) // if submission does not exist
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
		String submissionId = comment.getLinkId();
		String author = comment.getAuthor();
		String text = comment.getBody();

		int numReplies = comment.getReplies().size();
		int score = comment.getScore();
		int authorFlair = comment.getAuthorFlair();

		Double created = comment.getCreated();
		// Analyze if the delta has received a comment, and get the explanation
		JSONObject deltaObject = deltaBot(comment);
		String explanation = (String) deltaObject.get("explanation");
		String deltaAwardedBy = (String) deltaObject.get("author");
		int deltaAwarded = (Integer) deltaObject.get("deltaAwarded");

		String sql = "INSERT INTO "
				+ tableName
				+ " (CID, SID, Author, Text, NumReplies, Score, AuthorFlair, Created, DeltaAwarded,  DeltaAwardedBy, Explanation) "
				+ "VALUES ('" + commentId + "','" + submissionId + "','"
				+ author + "','" + text.replace("\'", "\'\'") + "','"
				+ numReplies + "','" + score + "','" + authorFlair + "','"
				+ created + "','" + deltaAwarded + "','" + deltaAwardedBy
				+ "','" + explanation.replace("\'", "\'\'") + "')";

		Statement stmt = connection.createStatement();
		stmt.executeUpdate(sql);
	}// end of add


	/**
	 * updates an existing comment if any changes has happened
	 * @param comment
	 * @throws SQLException
	 */
	public static void updateComment(Comment comment) throws SQLException {
		// get the old record
		boolean textFlg, repliesFlg, scoreFlg, authorFlg, deltaAwardedFlg, explanationFlg, awardedByFlg = false;
		String commentId = comment.getIdentifier();
		Statement stmt = connection.createStatement();
		String sql = "SELECT * FROM " + tableName + " WHERE CID='" + commentId
				+ "'";
		ResultSet rs = stmt.executeQuery(sql);
		if (rs.next()) {
			// new information from server
			String text = comment.getBody();
			int numReplies = comment.getReplies().size();
			int score = comment.getScore();
			int authorFlairText = comment.getAuthorFlair();
			JSONObject deltaObject = deltaBot(comment);
			String explanation = (String) deltaObject.get("explanation");
			String deltaAwardedBy = (String) deltaObject.get("author");
			int deltaAwarded = (Integer) deltaObject.get("deltaAwarded");

			// old information from database
			String oldText = rs.getString("Text");
			String oldExplanation = rs.getString("Explanation");
			String oldDeltaAwardedBy = rs.getString("DeltaAwardedBy");
			int oldDeltaAwarded = rs.getInt("DeltaAwarded");
			int oldNumReplies = rs.getInt("NumReplies");
			int oldScore = rs.getInt("Score");
			int oldAuthorFlairText = rs.getInt("AuthorFlair");
			// compare information
			System.out.println("***changes:");
			textFlg = compareString("Text", oldText, text);
			awardedByFlg = compareString("AwardedBy", oldDeltaAwardedBy,
					deltaAwardedBy);
			explanationFlg = compareString("Explanation", oldExplanation,
					explanation);
			deltaAwardedFlg = compareInt("DeltaAwarded", oldDeltaAwarded,
					deltaAwarded);
			repliesFlg = compareInt("NumReplies", oldNumReplies, numReplies);
			scoreFlg = compareInt("Score", oldScore, score);
			authorFlg = compareInt("AuthorFlair", oldAuthorFlairText,
					authorFlairText);
			// if any changes, update
			if (textFlg || repliesFlg || scoreFlg || authorFlg
					|| explanationFlg || deltaAwardedFlg || awardedByFlg) {
				sql = "UPDATE " + tableName + " SET " + "Text='"
						+ text.replace("\'", "\'\'") + "', NumReplies="
						+ numReplies + ", Score=" + score + ", AuthorFlair="
						+ authorFlairText + ", DeltaAwarded=" + deltaAwarded
						+ ", DeltaAwardedBy='" + deltaAwardedBy
						+ "', Explanation='"
						+ explanation.replace("\'", "\'\'") + "' WHERE CID='"
						+ commentId + "'";
				stmt.executeUpdate(sql);
				System.out.println("Comment updated");
			}
			if (authorFlg) {
				UserCollector user = new UserCollector("reddit_cmv");
				user.updateAuthorFlair(comment.getAuthor(), authorFlairText);
			}
		}// if for reading from database
	}

	/**
	 * Gets a comment entity and analyzes its comments to the depth of two to check if 
	 * the deltaBot has confirmed the delta point
	 * @param comment
	 * @return a JSON object with the delta information, its explanation, and the author who is awarding delta
	 * delta is 1 if awarded, and 0 if not
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
	 * Retrieves all the comments for each submission in the submissions table
	 * and adds them to the database (Delta is 1 if awarded, 0 if not)
	 * @param restClient
	 * @param user
	 * @throws SQLException
	 */
	public void getSubmissionComments()
			throws SQLException {
		connect();
		ResultSet submissions = returnAll("submissions");
		Comments cmnts = new Comments(restClient, user);
		int iterations = 0; // each submission
		// for each submission in the submissions' table
		while (submissions.next()) 
		{
			try {
				//updating iterations
				System.out.println("--------------Submission " + ++iterations); 
				// submissionId for the comment  does not have "t3_" in reddit API
				String submissionId = submissions.getString("SID").substring(3); 
				List<Comment> comments = cmnts.ofSubmission(submissionId, null,
						-1, -1, 1000, CommentSort.NEW);
				System.out.println(comments.size());
				// for each comment of a submission
				for (int i = 0; i < comments.size(); i++) 
				{
					Comment comment = comments.get(i);
					System.out.println("----Comment " + (i + 1));
					System.out.println("parent: " + comment.getParentId());
					System.out.println("author: " + comment.getAuthor());
					addOrUpdateComment(comment);
				}
			} catch (RetrievalFailedException e) {
				e.printStackTrace();
				continue;
			} // if comment retrieval failed for some reason, continue

		}
	}
}
