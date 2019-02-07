package com.github.jreddit.changemyview;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.json.simple.parser.ParseException;

import com.github.jreddit.entity.User;
import com.github.jreddit.utils.restclient.HttpRestClient;
import com.github.jreddit.utils.restclient.RestClient;

/**
 * @author Taraneh
 * All the collectors inherit from Database
 * Therefore, reddit user connection and database connection are made here
 */
public class Database {

	RestClient restClient = new HttpRestClient();
	String redditUserName="cmvProject";
	String redditPassword="cmvcmv";
	User user = new User(restClient, redditUserName, redditPassword);
	private String databaseName = "reddit_cmv";
	private String userName = "root";
	private String password = "";
	private String url = "jdbc:mysql://localhost:3306/";
	protected static Connection connection = null;

	public Database() throws IOException, ParseException {
		restClient.setUserAgent("bot/1.0 by name");
		user.connect();
	}

	public Database(String databaseName) {
		this.databaseName = databaseName;
	}

	public Database(String databaseName, String userName, String password) {
		this.databaseName = databaseName;
		this.userName = userName;
		this.password = password;
	}

	// ----------------------------------
	public void connect() {
		try {
			Database.connection = DriverManager.getConnection(url + databaseName,
					userName, password);
		} catch (SQLException ex) {
			// handle any errors
			System.out.println("SQLException: " + ex.getMessage());
			System.out.println("SQLState: " + ex.getSQLState());
			System.out.println("VendorError: " + ex.getErrorCode());
		}
	}

	// ---------------------------------------
	public Connection getConnection() {
		return connection;
	}

	// ---------------------------------------

	public void truncate(String tableName) throws SQLException {
		Statement stmt = connection.createStatement();
		String sql = "TRUNCATE TABLE " + tableName;
		stmt.executeUpdate(sql);
	}

	/**
	 * @param tableName
	 * @param field
	 * @param value
	 * @return a boolean value representing whether the field-value pair exists
	 *         in the table
	 * @throws SQLException
	 */
	public int count(String tableName, String field, String value)
			throws SQLException {
		Statement stmt = connection.createStatement();
		String sql = "SELECT COUNT(*) AS total FROM " + tableName + " WHERE "
				+ field + "='" + value + "'";
		ResultSet rs = stmt.executeQuery(sql);
		if (rs.next());
		return rs.getInt("total");
	}
	/**
	 * Deletes from a table when a field matches a value
	 * For example, delete all the comments made by moderators
	 * @param tableName
	 * @param field
	 * @param value
	 * @return
	 * @throws SQLException
	 */
	public void delete(String tableName, String field, String value)
			throws SQLException {
		Statement stmt = connection.createStatement();
		String sql = "DELETE FROM " + tableName + " WHERE "
				+ field + "='" + value + "'";
		stmt.executeQuery(sql);
	}

	/**
	 * Compares two integer values and if they are not the same, returns false
	 * and prints a message (suitable for updates)
	 * 
	 * @param field
	 * @param databaseValue
	 * @param currentValue
	 * @return a boolean value representing of two integers are equal
	 */
	protected static boolean compareInt(String field, int databaseValue,
			int currentValue) {
		if (databaseValue != currentValue) {
			System.out.println(field + " is changed from " + databaseValue
					+ " to " + currentValue);
			return true;
		} else {
			return false;
		}
	}

	/**
	 * Compares two string values (suitable for updates)
	 * 
	 * @param field
	 * @param databaseValue
	 * @param currentValue
	 * @return a boolean value representing if two Strings are equal
	 */
	protected static boolean compareString(String field, String databaseValue,
			String currentValue) {
		if (currentValue != null && !databaseValue.equals(currentValue)) {
			if (field.equals("Text"))
				System.out.println(field + " is changed");
			else
				System.out.println(field + " is changed from " + databaseValue
						+ "(" + databaseValue.length() + ")" + " to "
						+ currentValue + "(" + currentValue.length() + ")");
			return true;

		} else {
			return false;
		}
	}

	/**
	 * @param tableName
	 * @return all the records in a table
	 * @throws SQLException
	 */
	public ResultSet returnAll(String tableName) throws SQLException {
		Statement stmt = connection.createStatement();
		String sql = "SELECT * FROM " + tableName;
		ResultSet rs = stmt.executeQuery(sql);
		return rs;
	}
	// ------------------------------
}
