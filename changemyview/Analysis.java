package com.github.jreddit.changemyview;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

import org.apache.commons.lang3.StringUtils;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.PorterStemFilter;
import org.apache.lucene.analysis.StopAnalyzer;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.OffsetAttribute;
import org.apache.lucene.analysis.tokenattributes.TermAttribute;
import org.apache.lucene.search.spell.PlainTextDictionary;
import org.apache.lucene.search.spell.SpellChecker;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.json.simple.parser.ParseException;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
/**
 * The analysis class handles statistical analysis and adds calculated information either to the SQL tables 
 * or the CSV files used by WEKA 
 * @author Taraneh
 *
 */
public class Analysis extends Database{
		
	public Analysis() throws IOException, ParseException {
		super();
		// TODO Auto-generated constructor stub
	}
	/**
	 * Add length information for comments in the source table (SQL)
	 * @param sourceTable
	 * @throws SQLException
	 */
	//add information to SQL
	public void addLength(String sourceTable) throws SQLException
	{
		connect();
		ResultSet comments=returnAll(sourceTable);
		Statement stmt = connection.createStatement();
		while(comments.next())
		{
			if(comments.getObject("length")==null)
			{
				String id=comments.getString("CID");
				String text=comments.getString("Text");
				int length=text.length();
			
				String sql = "UPDATE " + sourceTable + " SET " + "Length='"
					+ length  + "' WHERE CID='"
					+ id + "'";
				stmt.executeUpdate(sql);
				System.out.println("Comment "+id+" updated with length: "+length);
			}
		}
		
	}
	//add information to SQL
	public void addDuration(String sourceTable) throws SQLException
	{
		connect();
		ResultSet users=returnAll(sourceTable);
		Statement stmt = connection.createStatement();
		while(users.next())
		{
			if(users.getObject("Duration")==null)
			{
				String id=users.getString("UID");
				Double created=users.getDouble("created");
				Double now=(double) System.currentTimeMillis()/1000;
				Double doubleDuration=now-created;
				int duration=(int) Math.ceil(doubleDuration/86400);
				String sql = "UPDATE " + sourceTable + " SET " + "Duration='"
						+ duration  + "' WHERE UID='"
						+ id + "'";
					stmt.executeUpdate(sql);		
				System.out.println("User info updated for"+ id +"for the duration of "+ duration +" days");
			}
		}
		
	}//---
//------------------------------------
	/**
	 * Reads each individual file
	 * @param path
	 * @return
	 * @throws IOException
	 */
	public String readFile(String path) throws IOException
	{
		  byte[] encoded = Files.readAllBytes(Paths.get(path));
		  return new String(encoded, Charset.defaultCharset());
	}
	/**
	 * loops through individual documents that represent each message
	 * Note that persuasive and np5 is from p1 to p1720 and non-persuasive is from np0-np1719 (no be fixed!)
	 * @return arraylist of referrals for each document
	 * @throws IOException 
	 */
	public ArrayList<Double> calculateReferral(String folderPath, String type, int start, int end) throws IOException
	{
		ArrayList<Double> referralPercentage=new ArrayList<Double>();
		//String type="p";
		//int start=type.equals("p")?1:0;		
		//int end=type.equals("p")?1720:1719;
		for(;start<=end;start++)
		{
			System.out.println("---------"+type+start);
			String content=readFile("data/classification_surface/"+folderPath+"/"+type+start+".txt");
			double blockCount = (double) StringUtils.countMatches(content, "\n\n")+1;
			double referralCount = (double) StringUtils.countMatches(content, "&gt;");
			double percentage=referralCount/blockCount;
			System.out.println(referralCount);
			System.out.println(blockCount);
			System.out.println(percentage);
			referralPercentage.add(percentage);
		}
		return referralPercentage;
	}
	/**
	 * Counts the blocks
	 * @param folderPath
	 * @param type
	 * @param start
	 * @param end
	 * @return
	 * @throws IOException
	 */
	public ArrayList<Double> calculateBlocks(String folderPath, String type, int start, int end) throws IOException
	{
		ArrayList<Double> blockCounts=new ArrayList<Double>();
		//String type="p";
		//int start=type.equals("p")?1:0;		
		//int end=type.equals("p")?1720:1719;
		for(;start<=end;start++)
		{
			System.out.println("---------"+type+start);
			String content=readFile("data/classification_surface/"+folderPath+"/"+type+start+".txt");
			double blockCount = (double) StringUtils.countMatches(content, "\n\n")+1;
			blockCounts.add(blockCount);
		}
		return blockCounts;
	}
	public ArrayList<Double> calculateMisspelled(String folderPath, String type, int start, int end) throws IOException
	{
		ArrayList<Double> misspelledCounts=new ArrayList<Double>();
		File dir = new File("/eDic/");
		Directory directory = FSDirectory.open(dir);
		SpellChecker spell= new SpellChecker(directory);
		spell.indexDictionary(new PlainTextDictionary(new File("eDic/fulldictionary00.txt")));
		for(;start<=end;start++)
		{
			System.out.println("---------"+type+start);
			String content=readFile("data/classification_surface/"+folderPath+"/"+type+start+".txt");
			advancedTextCleaner cleaner=new advancedTextCleaner();
			System.out.println("1. content: "+content);
			content=content.replaceAll("\\\\", "");
			content=cleaner.toLowerCase(content);
			content=cleaner.elisionControl(content);
			content=cleaner.removeHTMLtags(content);
			
			try{
				content=cleaner.removeUrl(content);
			}
			catch(java.util.regex.PatternSyntaxException e){e.printStackTrace();}
			catch(java.lang.NullPointerException e){e.printStackTrace();}
			content=cleaner.removeStopWords(content);
			content=content.replaceAll("[^A-Za-z ]", "");
			content=cleaner.removeExtraSpace(content);
			
		    System.out.println("2. content: "+content);
			String[] words=content.split(" ");
			int count=0;
			for(String word:words)
			{
				word=cleaner.removeExtraSpace(word);
				if(!spell.exist(word))
					{
						count++;
						System.out.println(word);
						//managing plurals
						if(word.endsWith("s") && spell.exist(word.substring(0,word.lastIndexOf("s"))))
						{
							count--;
							System.out.println(word.substring(0,word.lastIndexOf("s"))+ " **is in");
						}
						//managing ed 
						if(word.endsWith("ed") && spell.exist(word.substring(0,word.lastIndexOf("ed"))))
						{
							count--;
							System.out.println(word.substring(0,word.lastIndexOf("ed"))+ " **is in");
						}
						//managing plural
						if(word.endsWith("ies") && spell.exist(word.substring(0,word.lastIndexOf("ies"))+"y"))
						{
							count--;
							System.out.println(word.substring(0,word.lastIndexOf("ies"))+"y"+ " **is in");
						}
						//ing and er
						
					}
				
			}
			System.out.println(count);
			double dCount=(double) count;
			System.out.println(dCount);
			double dLength=(double) words.length;
			System.out.println(dLength);
			double ratio=dCount/dLength;
			System.out.println(ratio*100);
			misspelledCounts.add(ratio*100);
		}
		return misspelledCounts;
	}
	/**
	 * Can be merged with blocks in code cleaning 
	 * @param folderPath
	 * @param type
	 * @param start
	 * @param end
	 * @return
	 * @throws IOException
	 */
	public ArrayList<Double> calculateURLS(String folderPath, String type, int start, int end) throws IOException
	{
		ArrayList<Double> URLCounts=new ArrayList<Double>();
		for(;start<=end;start++)
		{
			System.out.println("---------"+type+start);
			String content=readFile("data/classification_surface/"+folderPath+"/"+type+start+".txt");
			double count1 = (double) StringUtils.countMatches(content, "http://");
			double count2 = (double) StringUtils.countMatches(content, "https://");
			double URLCount=count1+count2;
			URLCounts.add(URLCount);
		}
		return URLCounts;
	}
	/**
	 * adds a column to the csv file
	 * @param inputPath is the old csv
	 * @param outputPath is the new csv 
	 * @param title is the title of the column
	 * @param values contains the values of the column
	 * @throws IOException
	 */
	public void addColumnCSV(String inputPath, String outputPath, String title, ArrayList<Double> values) throws IOException
	{
		System.out.println("--------------");
		System.out.println("Start writing...");
		System.out.println("size "+values.size());
		String basePath="data/classification_surface";
		String input=basePath+inputPath;
		String output=basePath+outputPath;
		CSVReader reader = new CSVReader(new FileReader(input));
		CSVWriter writer = new CSVWriter(new FileWriter(output), ',');
		String[] entries = null;
		int i=0; //for looping through values
		while ((entries = reader.readNext()) != null)
		{
		    ArrayList list = new ArrayList(Arrays.asList(entries));
		    if(list.get(0).equals("Filename")) 
		    {
		    	list.add(title);
		    } // Add the new element here
		    else 
		    {
		    	System.out.println(values.get(i));
		    	list.add(values.get(i).toString());
		    	 i++; //for looping through values
		    }
		    String[] row = (String[]) list.toArray(new String[list.size()]);
		    writer.writeNext(row);
		   
		}
		writer.close();
		System.out.println("Done!!");
		System.out.println(i);
	}
	//----------------
	
	//-----
	

}
