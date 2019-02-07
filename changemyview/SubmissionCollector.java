package com.github.jreddit.changemyview;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.List;

import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

import com.github.jreddit.entity.Submission;
import com.github.jreddit.retrieval.Submissions;
import com.github.jreddit.retrieval.params.SubmissionSort;

import static com.github.jreddit.utils.restclient.JsonUtils.safeJsonToString;

public class SubmissionCollector extends Database {

	private String tableName = "submissions";

	public SubmissionCollector(String databaseName, String userName, String password) {
		super(databaseName, userName, password);
	}

	public SubmissionCollector(String databaseName) {
		super(databaseName);
	}

	public SubmissionCollector() throws IOException, ParseException {
		super();
	}

	/**
	 * Gets a submission entity and checks if it exists in the database
	 * If it does, adds it to the database
	 * If not, updates the record if any changes have happened
	 * @param submission
	 * @throws SQLException
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public void addOrUpdateSubmission(Submission submission)
			throws SQLException, IOException, ParseException {
		String fullName = submission.getFullName();
		if (count(tableName, "SID", fullName) == 0) // if the submission does
													// not exist
		{
			System.out.println("Adding the new submission...");
			addSubmission(submission);
		} else // if the submission already exists
		{
			System.out.println("the submission already exists!");
			updateSubmission(submission);
		}

	}
	/**
	 * adds a submission entity to the table
	 * @param submission
	 * @throws SQLException
	 */
	public void addSubmission(Submission submission) throws SQLException {
		String fullName = submission.getFullName();
		String title = submission.getTitle();
		String author = submission.getAuthor();
		String text = submission.getSelftext();
		Long numComments = submission.getCommentCount();
		Long score = submission.getScore();
		Double created = submission.getCreated();
		String link = submission.getPermalink();
		String linkFlairText = submission.getLinkFlairText();
		int authorFlairText = submission.getAuthorFlair();

		String sql = "INSERT INTO "
				+ tableName
				+ " (SID, Title, Author, Text, NumComments, Score, Created, Link, LinkFlair, AuthorFlair) "
				+ "VALUES ('" + fullName + "','" + title.replace("\'", "\'\'")
				+ "','" + author + "','" + text.replace("\'", "\'\'") + "','"
				+ numComments + "','" + score + "','" + created + "','" + link
				+ "','" + linkFlairText + "','" + authorFlairText + "')";

		Statement stmt = connection.createStatement();
		stmt.executeUpdate(sql);
	}

	/**
	 * updates a submission record in the table if it attributes have changed
	 * @param submission
	 * @throws SQLException
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public void updateSubmission(Submission submission) throws SQLException, IOException, ParseException {
		// get the old record
		boolean textFlg, linkFlg, commentFlg, scoreFlg, authorFlg = false;
		String fullName = submission.getFullName();
		Statement stmt = connection.createStatement();
		String sql = "SELECT * FROM " + tableName + " WHERE SID='" + fullName
				+ "'";
		ResultSet rs = stmt.executeQuery(sql);
		if (rs.next()) {
			// new information from server
			String text = submission.getSelftext();
			Long numComments = submission.getCommentCount();
			Long score = submission.getScore();
			String linkFlairText = submission.getLinkFlairText();
			int authorFlairText = submission.getAuthorFlair();
			// old information from database
			String oldText = rs.getString("Text");
			String oldLinkFlairText = rs.getString("LinkFlair");
			int oldNumComments = rs.getInt("NumComments");
			int oldScore = rs.getInt("Score");
			int oldAuthorFlairText = rs.getInt("AuthorFlair");
			// compare information
			System.out.println("***changes:");
			textFlg = compareString("Text", oldText, text);
			linkFlg = compareString("LinkFlair", oldLinkFlairText,
					linkFlairText);
			commentFlg = compareInt("NumComments", oldNumComments,
					(int) (numComments.longValue()));
			scoreFlg = compareInt("Score", oldScore, (int) (score.longValue()));
			authorFlg = compareInt("AuthorFlair", oldAuthorFlairText,
					authorFlairText);
			// if any changes, update
			if (textFlg || linkFlg || commentFlg || scoreFlg || authorFlg) {
				sql = "UPDATE " + tableName + " SET " + "Text='"
						+ text.replace("\'", "\'\'") + "', LinkFlair='"
						+ linkFlairText + "', NumComments=" + numComments
						+ ", Score=" + score + ", AuthorFlair="
						+ authorFlairText + " WHERE SID='" + fullName + "'";
				stmt.executeUpdate(sql);
				System.out.println("Submission updated");
			}
			// if authors' delta points have changed, update the user info the
			// user table
			if (authorFlg) {
				UserCollector user = new UserCollector();
				user.updateAuthorFlair(submission.getAuthor(), authorFlairText);
			}
		}// if for reading from database
	}

	/**
	 * Retrieves all the new submissions from the changemyview subreddit and adds or updates them
	 * @param restClient
	 * @param user
	 * @throws SQLException
	 * @throws ParseException 
	 * @throws IOException 
	 */
	public void getSubmissions()
			throws SQLException, IOException, ParseException {
		connect();
		// retrieve submissions
		Submissions subms = new Submissions(restClient, user);
		DateFormat format = new SimpleDateFormat("yy/M/dd hh:mm a");
		int count = 0; // no submission has been collected yet
		Submission after = null;
		int iterations = 0;
		do {
			List<Submission> submissionsSubreddit = subms.ofSubreddit(
					"changemyview", SubmissionSort.NEW, count, 100, after,
					null, true);
			// if the new set of submissions is empty, break the loop
			if (submissionsSubreddit.size() == 0) {
				System.out.println("----No more submissions available----");
				break;
			}
			// for each post in the current iteration
			for (int i = 0; i < submissionsSubreddit.size(); i++) {
				count = (iterations * 100) + (i + 1);
				System.out.println("------New item: " + (i + 1)
						+ "------Total: " + count);
				
				Submission submission = submissionsSubreddit.get(i);
				after = submission; // updating after
				double submissionDate = submission.getCreated();
				System.out.println("SID: " + submission.getFullName());
				System.out.println(submission.getTitle());
				System.out.println(format.format(submissionDate * 1000));
				System.out.println("UID: " + submission.getAuthor());
				System.out.println("LinkFlair: "
						+ submission.getLinkFlairText());
				addOrUpdateSubmission(submission);
			}// end of for
			++iterations; // next iteration of reading data (100 posts)
		} while (true);
	}// end of submission
}
