package com.github.jreddit.changemyview;
import java.io.IOException;
import java.net.MalformedURLException;
import java.sql.SQLException;




import java.util.ArrayList;

import org.json.simple.parser.ParseException;




public class Main {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		//operations with the data
		//------------------------
		//retrieve submission from CMV
		//SubmissionCollector submissions=new SubmissionCollector();
		//submissions.getSubmissions();
		
		//for each submission, retrieve comments
		//SubmissionCommentCollector submissionComments=new SubmissionCommentCollector();
		//submissionComments.getSubmissionComments();
		
		//for each entity (submission and/or comments), retrieve user information 
		/*UserCollector users=new UserCollector();
		users.getUsers("submissions");
		users.getUsers("submission_comments");*/
		
		/*for each user, retrieve comments
		 * after comments are retrieved, the user table needs to be updated
		 * for the number of comment made into cmv to be updated
		 * As well, user_comments need to be updated by delta related values
		 * that are missing when we extract user_comments, but are availbe when extracting
		 * submission comments
		 * UPDAING this tables is not as straightforward as submissions/users/and submission_comments:
		 * Updates are checked for score and text
		 * if delta information needs to be updated, fillExtraAttributes() should be used again
		 * if users table needs to be update with new cmvComments, then updateUserCMVCommentInfo should be used
		 */
		
		//UserCommentCollector userComments=new UserCommentCollector();
		//userComments.getUserComments("users");
		
		//fill the missing information
		//userComments.fillExtraAttributes();
		//update all the cmvCounts in the users table
		
		//UserCollector userRecord = new UserCollector();
		//userRecord.updateUserCMVcommentInfo();
		
		/*filter users based criteria specified in the corresponding classes
		 * and fills new persuasive and nonpersuasive tables
		 */
		/*UserSelector pUsers=new UserSelector("persuasive");
		pUsers.dumpSelectedUsers();*/
		/*UserSelector npUsers=new UserSelector("nonpersuasive");
		npUsers.dumpSelectedUsers();*/
		
		//get user comment from the corresponding tables
		/*SelectedUserComments puc=new SelectedUserComments("persuasive");
		puc.getUserComments();*/
		/*SelectedUserComments npuc=new SelectedUserComments("nonpersuasive");
		npuc.getUserComments();*/
		
		
		Analysis analyze=new Analysis();
		//analyze.addLength("submission_comments");
		//analyze.addDuration("nonpersuasive_users");
		
		//np1 - np 4 ---> 0-1719
		//p and np5 ---> 1-1720
		
		//ArrayList<Double> values=analyze.calculateReferral("np4","np",0,1719);
		//analyze.addColumnCSV("/referrals/LIWC2007 Results-allnp4.csv","/referrals/LIWC2007 Results-allnp4_referrals.csv","Referral",values);
		
		//ArrayList<Double> values=analyze.calculateBlocks("p","p",1,1720);
		//analyze.addColumnCSV("/referrals/LIWC2007 Results-allp_referrals.csv","/referrals/LIWC2007 Results-allp_referrals_blocks.csv","Blocks",values);
		
		//ArrayList<Double> values=analyze.calculateURLS("np4","np",0,1719);
		//analyze.addColumnCSV("/referrals/LIWC2007 Results-allnp4_referrals_blocks.csv","/referrals/LIWC2007 Results-allnp4_referrals_blocks_urls.csv","URLS",values);
		
		ArrayList<Double> values=analyze.calculateMisspelled("p","p",1,1720);
		//analyze.addColumnCSV("/finalClassification/LIWC2007 Results-allnp1_referrals_blocks_urls.csv","/finalClassification/LIWC2007 Results-allnp1_referrals_blocks_urls_mssp.csv","Misspelled",values);
		
		
		//----------------------------------
		//LIWCInputGenerator liwc=new LIWCInputGenerator("data/persuasiveComments_1720 (union without duplicates).csv"
		//		,"data/p_test1_csv","p");
		//liwc.writeAll();
		//------------------------------------
		
	}//end of main
	
}
