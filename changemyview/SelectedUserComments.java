package com.github.jreddit.changemyview;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;



public class SelectedUserComments extends Database {

	String sourceTable2Name="user_comments";
	String sourceTable1Name="";
	String targetTableName="";
	
	public SelectedUserComments(String userType) throws Exception {
		
		if(userType.equals("persuasive"))
		{
			sourceTable1Name="persuasive_users";
			targetTableName="persuasive_user_comments";
		}
		else if(userType.equals("nonpersuasive"))
		{	
			sourceTable1Name="nonpersuasive_users";
			targetTableName="nonpersuasive_user_comments";
		}
		else
		{
			throw new Exception("wrong argument is passed to select users: it can be either persuasive or nonpersuasive");
		}
	}
	//------------------------------------------------------
	public void getUserComments() throws SQLException
	{
		connect();
		ResultSet users=returnAll(sourceTable1Name);
		while(users.next())
		{
			//get userName
			String userName=users.getString("UserName");
			System.out.println("---------------------");
			System.out.println("comments for "+userName);
			//get all the comments from that user from user_comments table
			ResultSet comments=getCommentsByUserName(userName);
			//dump all the comments to the comment table
			CommentsToTable(comments);
		}
		
	}
	//--------------------------------------------------
	public ResultSet getCommentsByUserName(String userName) throws SQLException
	{
		Statement stmt = connection.createStatement();
		String sql = "SELECT * FROM " + sourceTable2Name +" where Author='"+userName+"';";
		ResultSet rs = stmt.executeQuery(sql);
		return rs;
	}
	//---------------------------------------------------
	public void CommentsToTable(ResultSet comments) throws SQLException
	{
		String sql = "";
		Statement stmt = connection.createStatement();
		while (comments.next()) {
			String CID = comments.getString("CID");
			String parentID = comments.getString("ParentID");
			String created = comments.getString("Created");
			String author = comments.getString("Author");
			String text = comments.getString("Text");
			int score = comments.getInt("Score");
			
			sql = "INSERT INTO "
					+ targetTableName
					+ " (CID, ParentID, Created, Author, Text, Score)"
					+ "VALUES ('" + CID + "','" + parentID + "','" + created
					+ "','" + author + "','" + text.replaceAll("\'", "\'\'") + "','"
					+ score + "')";
			stmt.executeUpdate(sql);
			System.out.println("comment added");
		}
	}
}

	
	
	

