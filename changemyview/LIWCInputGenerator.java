package com.github.jreddit.changemyview;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.opencsv.CSVReader;

public class LIWCInputGenerator {
	
	String path="";
	String column="";
	String wPath="";
	String type="";
	LIWCInputGenerator(String CSVPath, String writePath, String commentType)
	{
		path=CSVPath;
		//column=columnName; Text is the second column and is accessed through index 
		wPath=writePath;
		type=commentType;
	}
	//reads CSV and dumps it into a list of arrays, each array is associated with a record 
	List readCSV() throws IOException
	{
		CSVReader reader = new CSVReader(new FileReader(path));
	    //List entries = reader.readAll();
		ArrayList<String> entries=new ArrayList<String>();
		String [] nextLine;
	    while ((nextLine = reader.readNext()) != null) {
	        // nextLine[] is an array of values from the line
	        entries.add(nextLine[1]);
	     }
	    System.out.println("Data is in...");
	    return entries;
	}
	List readJSON() throws FileNotFoundException, IOException, ParseException 
	{
		ArrayList<String> entries=new ArrayList<String>();
		JSONParser parser=new JSONParser();
		Object obj = parser.parse(new FileReader(path));
		JSONArray jsonArray = (JSONArray) obj;
		for(int i=0;i<jsonArray.size();i++)
		{
			JSONObject object=new JSONObject(); 
			object=(JSONObject) jsonArray.get(i);
			String comment = (String) object.get("Text");
			System.out.println(i+"------");
			entries.add(comment);
        }
		System.out.println("Data is in...");
		return entries;
	}
	//creates a txt file and writes the name into that 
	void writeComment(String comment, String name) throws FileNotFoundException, UnsupportedEncodingException
	{
		PrintWriter writer = new PrintWriter(wPath+"/"+name+".txt", "UTF-8");
		writer.println(comment);
		writer.close();
	}
	//for each comment, runs writeComment
	void writeAll() throws IOException, ParseException
	{
		List list=readCSV();
		//List list=readJSON();
		System.out.println("Writing....");
		System.out.println("Size: "+ list.size());
		
		for(int i=0;i<list.size();i++)
		{
			//String[] record=(String[]) list.get(i);
			//the textual information is located at index 1 of the array!
			System.out.println(i+" -----------");
			//System.out.println(record.length);
			//System.out.println(record[0]);
			String comment=(String) list.get(i);
			writeComment(comment,type+Integer.toString(i));
		}
		System.out.println("Done!");
	}

}