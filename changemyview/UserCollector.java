package com.github.jreddit.changemyview;
import java.io.IOException;
import java.math.RoundingMode;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DecimalFormat;

import org.json.simple.parser.ParseException;

import com.github.jreddit.action.ProfileActions;
import com.github.jreddit.entity.UserInfo;
import com.github.jreddit.exception.ActionFailedException;
import com.github.jreddit.exception.RetrievalFailedException;

public class UserCollector extends Database {

	String tableName = "users";

	public UserCollector(String databaseName, String userName, String password) {
		super(databaseName, userName, password);
	}

	public UserCollector(String databaseName) {
		super(databaseName);
	}

	public UserCollector() throws IOException, ParseException {
		super();
	}

	/**
	 * Gets a user entity and checks if it exists in the database
	 * If it does, adds it to the database
	 * If not, updates the record if any changes have happened
	 * @param user
	 * @param delta is the delta points associated with the user retrieved from comments or submissions
	 * @throws SQLException
	 */
	public void addOrUpdateUser(UserInfo user, int delta) throws SQLException {
		String userID = user.getId();
		if (count(tableName, "UID", userID) == 0) // if submission does not
													// exist
		{
			System.out.println("Adding the new user...");
			addUser(user, delta);
		} else // if submission already exists
		{
			System.out.println("the user already exists!");
			updateUser(user);
		}

	}

	/**
	 * updates user if changed
	 * @param user
	 * @throws SQLException
	 */
	public void updateUser(UserInfo user) throws SQLException {
		boolean cmntKarmaFlg, linkKarmaFlg;
		String id = user.getId();
		Statement stmt = connection.createStatement();
		String sql = "SELECT * FROM " + tableName + " WHERE UID='" + id + "'";
		ResultSet rs = stmt.executeQuery(sql);
		if (rs.next())
			;
		// new information from server
		Long linkKarma = user.getLinkKarma();
		Long commentKarma = user.getCommentKarma();
		// old information from database
		int oldLinkKarma = rs.getInt("LinkKarma");
		int oldCommentKarma = rs.getInt("CommentKarma");
		// comparing...
		cmntKarmaFlg = compareInt("Link Karma", oldLinkKarma,
				(int) linkKarma.longValue());
		linkKarmaFlg = compareInt("Comment Karma", oldCommentKarma,
				(int) commentKarma.longValue());
		if (cmntKarmaFlg || linkKarmaFlg) {
			sql = "UPDATE " + tableName + " SET " + "LinkKarma='" + linkKarma
					+ "', CommentKarma='" + commentKarma + "' WHERE UID='" + id
					+ "'";
			stmt.executeUpdate(sql);
			System.out.println("User updated");
		}
	}

	/**
	 * adds a new user
	 * @param user
	 * @param delta
	 * @throws SQLException
	 */
	public void addUser(UserInfo user, int delta) throws SQLException {
		String id = user.getId();
		String userName = user.getName();
		Double created = user.getCreated();
		Long linkKarma = user.getLinkKarma();
		Long commentKarma = user.getCommentKarma();
		String sql = "INSERT INTO "
				+ tableName
				+ " (UID, UserName, Created, LinkKarma, CommentKarma, AuthorFlair) "
				+ "VALUES ('" + id + "','" + userName + "','" + created + "','"
				+ linkKarma + "','" + commentKarma + "','" + delta + "')";
		Statement stmt = connection.createStatement();
		stmt.executeUpdate(sql);
	}

	/**
	 * When collecting comments of a user, updates user information with their comment attributes
	 * such as their participationRatio and authorFlairRatio
	 * @param userName
	 * @param totalComments
	 * @param cmvComments
	 * @param authorFlair
	 * @throws SQLException
	 */
	public void updateUserTotalParticipation(String userName, int totalComments) throws SQLException {

		Statement stmt = connection.createStatement();
		String sql = "UPDATE " + tableName + " SET  TotalComments='" + totalComments
		+ "' WHERE UserName='" + userName + "'";
		stmt.executeUpdate(sql);
		System.out.println("User total participation updated in users table");
	}
	/**
	 * Once all the user comment are retrieved or updated! cmvComments count is updated for all users 
	 * by counting their number of comments in user_comments table as we may loose some of the cmv comments
	 * in reddit by time (only the newest 1000 comments made by the user can be retrieved)
	 * @param userName
	 * @param totalComments
	 * @param cmvComments
	 * @param authorFlair
	 * @throws SQLException
	 */
	//------------------------------------------
	public void updateUserCMVcommentInfo() throws SQLException {
		ResultSet users=returnAll("users");
		while(users.next())
		{
			String userName=users.getString("UserName");
			int totalComments=users.getInt("TotalComments");
			int authorFlair=users.getInt("AuthorFlair");
			int cmvComments=count("user_comments","Author",userName);
			System.out.println(userName+": "+cmvComments);
			
			DecimalFormat dc = new DecimalFormat("#.####");
			dc.setRoundingMode(RoundingMode.DOWN);
			double ratio=0;
			String sRatio="";
			double participationRatio=0;
			double authorFlairRatio=0;
	
			try
			{
				ratio = (double) cmvComments / (double) totalComments;
				sRatio = dc.format(ratio);
				participationRatio = Double.parseDouble(sRatio);
				authorFlairRatio = 0;
			}
			catch (java.lang.NumberFormatException e) {
				e.printStackTrace();
			}
			try {
				ratio = (double) authorFlair / (double) cmvComments;
				sRatio = dc.format(ratio);
				authorFlairRatio = Double.parseDouble(sRatio);
			}
			// if the user has not participated as a commenter (has only submitted)
			// and the cmvComments is 0
			catch (java.lang.NumberFormatException e) {
				e.printStackTrace();
			}
			
	
			Statement stmt = connection.createStatement();
			String sql = "UPDATE " + tableName + " SET " + "cmvComments='"
					+ cmvComments + "', ParticipationRatio='" + participationRatio
					+ "', AuthorFlairRatio='" + authorFlairRatio
					+ "' WHERE UserName='" + userName + "'";
			stmt.executeUpdate(sql);
			System.out.println("User comment info updated");
		}
	}
	//-----------------------------
	/**
	 * When collecting submissions and comments, if the authorFlair is changed
	 * the user information needs to be updated in the user table
	 * @param userName
	 * @param authorFlairText
	 * @throws SQLException
	 */
	public void updateAuthorFlair(String userName, int authorFlairText)
			throws SQLException {
		Statement stmt = connection.createStatement();
		String sql = "UPDATE " + "USERS" + " SET " + "AuthorFlair='"
				+ authorFlairText + "' WHERE UserName='" + userName + "'";
		stmt.executeUpdate(sql);
		System.out.println("AuthorFlair updated in USERS table for: "
				+ userName);
	}

	/**
	 * Retrieves the user information for all the users from the sourceTable  (e.g., submissions and comments)
	 * adds or updates this user info in the user table
	 * @param sourceTable
	 * @param restClient
	 * @param user
	 * @throws SQLException
	 */
	public void getUsers(String sourceTable)
			throws SQLException {
		System.out.println("Retrieving users from table: " + sourceTable);
		connect();
		ResultSet records = returnAll(sourceTable);
		ProfileActions pfs = new ProfileActions(restClient, user);
		int iterations = 0; // for each user
		// get users from submission list
		while (records.next()) {
			try {
				++iterations;
				System.out.println("------" + iterations + "--------User Name:"
						+ records.getString("Author"));
				UserInfo userInfo = pfs.about(records.getString("Author"));
				addOrUpdateUser(userInfo, records.getInt("AuthorFlair"));
				// if the user has been deleted, continue
			} catch (ActionFailedException e) 
			{
				e.printStackTrace();
				continue;
			}
			// if the user can not be retrieved, continue
			catch (RetrievalFailedException e) 
			{
				e.printStackTrace();
				continue;
			}
		}
	}

}
