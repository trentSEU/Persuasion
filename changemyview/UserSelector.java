package com.github.jreddit.changemyview;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.json.simple.parser.ParseException;

public class UserSelector extends Database {
	String tableName = "";
	int cmvComments=0;
	double authorFlairRatio=0;
	double maxAuthorFlairRatio=0;
	double authorFlair=0;
	String sqlQuery="";
	
 /**
  * 
  * @param userType can be either persuasive or nonpersuasive
 * @throws Exception 
  */
	public UserSelector(String userType) throws Exception {
		super();
		if(userType.equals("persuasive"))
				{
					tableName = "persuasive_users";
					cmvComments=5;
					authorFlairRatio=0.3052;
				    maxAuthorFlairRatio=1;
					sqlQuery = "SELECT * FROM USERS WHERE cmvComments>=" + cmvComments
							+ " AND AuthorFlairRatio>=" + authorFlairRatio +" AND AuthorFlairRatio<=" + maxAuthorFlairRatio;
				}
		else if(userType.equals("nonpersuasive"))
		{
			tableName = "nonpersuasive_users";
			cmvComments=93;
			authorFlair=0;
			sqlQuery = "SELECT * FROM USERS WHERE cmvComments>=" + cmvComments
					+ " AND AuthorFlair=" + authorFlair;
			
		}
		else
		{
			throw new Exception("wrong argument is passed to select users: it can be either persuasive or nonpersuasive");
		}
	}

	public ResultSet selectUsers()
			throws SQLException {
		Statement stmt = connection.createStatement();
		return stmt.executeQuery(sqlQuery);
	}

	public void dumpSelectedUsers() throws SQLException {
		
		connect();
		//clean the old table 
		truncate(tableName);
		ResultSet selectedUsers=selectUsers();
		UsersToTable(selectedUsers);
	}
	// ---------------------------------------
	public void UsersToTable(ResultSet selectedUsers) throws SQLException
	{
		String sql = "";
		Statement stmt = connection.createStatement();
		while (selectedUsers.next()) {
			String UID = selectedUsers.getString("UID");
			String userName = selectedUsers.getString("UserName");
			String created = selectedUsers.getString("Created");
			int linkKarma = selectedUsers.getInt("LinkKarma");
			int commentKarma = selectedUsers.getInt("CommentKarma");
			int authorFlair = selectedUsers.getInt("AuthorFlair");
			int cmvComments = selectedUsers.getInt("cmvComments");
			int totalComments = selectedUsers.getInt("TotalComments");
			double participationRatio = selectedUsers
					.getDouble("ParticipationRatio");
			double authorFlairRatio = selectedUsers
					.getDouble("AuthorFlairRatio");

			sql = "INSERT INTO "
					+ tableName
					+ " (UID, UserName, Created, LinkKarma, CommentKarma, AuthorFlair, cmvComments, TotalComments, ParticipationRatio, AuthorFlairRatio) "
					+ "VALUES ('" + UID + "','" + userName + "','" + created
					+ "','" + linkKarma + "','" + commentKarma + "','"
					+ authorFlair + "','" + cmvComments + "','" + 
					+ totalComments + "','" + participationRatio + "','"
					+ authorFlairRatio + "')";
			stmt.executeUpdate(sql);
			System.out.println("Selected user added: "+userName);
		}
	}

}
