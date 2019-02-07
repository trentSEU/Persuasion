package com.github.jreddit.changemyview;
import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.search.spell.PlainTextDictionary;
import org.apache.lucene.search.spell.SpellChecker;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.jsoup.Jsoup;


public class advancedTextCleaner {

	static HashMap<String,String> elision = new HashMap<String, String>();
	HashMap<String,String> emoticons=new HashMap<String,String>();
	//the elision hashmap gets filled in the constructor
	public advancedTextCleaner()
	{
		fillElision();
		fillEmoticons();
	}
	//removes html tags from text
	public String removeHTMLtags(String text)
	{
		  return Jsoup.parse(text).text();
	}
	//converts text to lower case
	public String toLowerCase(String text)
	{
		return text.toLowerCase();
	}
	//removes all extra spaces
	public static String removeExtraSpace(String text)
	{
		return text.trim().replaceAll(" +", " ");
	}
	//replaces all of the elisions using the hashmap
	public String elisionControl(String text)
	{
		 String newText="";
		 String[] textArray = text.split(" "); 
		 for (int i=0;i<textArray.length;i++) {
			 if(elision.containsKey(textArray[i]))
			 {
				 textArray[i]=elision.get(textArray[i]);
			 }
		  }
		 for(String s:textArray)
		 {
			 newText=newText+s+" ";
		 }
		 return removeExtraSpace(newText);
	}
	//replaces all of the elisions using the hashmap
	public String emoticonControl(String text)
	{
		 String newText="";
		 String[] textArray = text.split(" ");
		 for (int i=0;i<textArray.length;i++) {
			 if(emoticons.containsKey(textArray[i]))
			 {
				 textArray[i]=emoticons.get(textArray[i]);
			 }
		  }
		 for(String s:textArray)
		 {
			 newText=newText+s+" ";
		 }
		 return removeExtraSpace(newText);
	}
	//check if text has any alphabetical characters and has more than one word
	//if not, it is treated as if does not exists
	public boolean hasAlphabet(String text)
	{
		return text.contains("[a-zA-Z]+");
	}
	//remove URLS from string 
	public String removeUrl(String text)
    {
        /*String urlPattern = "((https?|ftp|gopher|telnet|file|Unsure|http):((//)|(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)";
        Pattern p = Pattern.compile(urlPattern,Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(text);
        int i = 0;
        while (m.find()) {
            text = text.replaceAll(m.group(i),"URL").trim();
            i++;
        }
        return text;*/
		return text.replaceAll("https?://\\S+\\s?", "").replaceAll("http?://\\S+\\s?", "").replaceAll("www?://\\S+\\s?", "");
    }
	//remove some punctuations
	public String removePunc(String text)
	{
		text=text.replaceAll("[^A-Za-z0-9.,;?!-\"() ]", "");
		text=text.replaceAll("!+", "!");
		text=text.replaceAll("\\?+", "\\?");
		text=text.replaceAll("\\.+", "\\. ");
		text=text.replaceAll("&", "and");
		return text;
				
	}
	//remove userName handler 
	public String removeHandler(String text)
	{
		return text.replaceAll("@\\p{L}+", "");
	}
	//check for misspeled words 
	public static void misspelled(String text) throws IOException
	{
		File dir = new File("/eDic/");
		Directory directory = FSDirectory.open(dir);
		SpellChecker spell= new SpellChecker(directory);
		spell.indexDictionary(new PlainTextDictionary(new File("eDic/fulldictionary00.txt")));
		String wordForSuggestions = "philanthropist";
		int suggestionsNumber = 5;
		System.out.println(spell.exist("philanthropist"));
		String[] suggestions = spell.suggestSimilar(wordForSuggestions, suggestionsNumber);
		if (suggestions!=null && suggestions.length>0) {
				 for (String word : suggestions) {
				                System.out.println("Did you mean:" + word);
				            }
		}

	}
	//removing stop words using Lucene 
	public String removeStopWords(String text) throws IOException
	{
		TokenStream tokenStream = new StandardTokenizer(Version.LUCENE_36, new StringReader(text));
		CharArraySet stopSet = CharArraySet.copy(Version.LUCENE_36, StandardAnalyzer.STOP_WORDS_SET);
		stopSet.add("i");
		stopSet.add("we");
		stopSet.add("up");
		stopSet.add("in");
		stopSet.add("my");
		stopSet.add("is");
		stopSet.add("do");
		stopSet.add("so");
		stopSet.add("us");
		stopSet.add("if");
		stopSet.add("it");
		stopSet.add("is");
		stopSet.add("he");
		stopSet.add("she");
		stopSet.add("they");
		stopSet.add("me");
		stopSet.add("go");
		stopSet.add("am");
		stopSet.add("as");
		tokenStream = new StopFilter(Version.LUCENE_36, tokenStream, stopSet);
		//tokenStream = new PorterStemFilter(tokenStream);
		//OffsetAttribute offsetAttribute = tokenStream.addAttribute(OffsetAttribute.class);
		CharTermAttribute token = tokenStream.getAttribute(CharTermAttribute.class);
		StringBuilder sb = new StringBuilder();
		while (tokenStream.incrementToken()) 
        {
            if (sb.length() > 0) 
            {
                sb.append(" ");
            }
            sb.append(token.toString());
        }
       return sb.toString();
	}
	//filling the elision hashmap
	public static void fillElision()
	{
		elision.put("i'm","i am");
		elision.put("i'll", "i will");
		elision.put("i'd", "i would");
		elision.put("i've", "i have");
		elision.put("you're","you are");
		elision.put("you've","you have");
		elision.put("you'll","you will");
		elision.put("you'd","you would");
		elision.put("she's","she has");
		elision.put("she'll","she will");
		elision.put("she'd","she would");
		elision.put("he's","he has");
		elision.put("he'll","he has");
		elision.put("he'd","he would");
		elision.put("we've","we have");
		elision.put("we'd", "we would");
		elision.put("we'll", "we will");
		elision.put("we're", "we are");
		elision.put("they've","they have");
		elision.put("they'd", "they would");
		elision.put("they'll", "they will");
		elision.put("they're", "they are");
		elision.put("it's","it is");
		elision.put("it'll", "it will");
		elision.put("it'd", "it would");
	
		elision.put("isn't","is not");
		elision.put("wasn't","was not");
		elision.put("won't", "will not");
		elision.put("don't","do not");
		elision.put("doesn't","does not");
		elision.put("did'nt", "did not");
		elision.put("aren't", "are not");
		elision.put("couldn't", "could not");
		elision.put("shouldn't", "should not");
		elision.put("ain't", "it would not");
		elision.put("would't", "would not");
		elision.put("hasn't", "has not");
		elision.put("haven't", "have not");
		elision.put("hadn't", "had not");
		
		elision.put("here's", "here is");
		elision.put("there's", "there is");
		elision.put("where's", "where is");
		elision.put("when's", "when is");
		elision.put("what's", "what is");
		
		elision.put("gonna","going to");
		elision.put("wanna", "want to");
		elision.put("gotta", "got to");
		elision.put("let's", "let us");
	}
	public void fillEmoticons()
	{
        emoticons.put(":)","smile");
        emoticons.put(":-)","smile");
        emoticons.put("=)","smile");
        emoticons.put(":D","smile-big");
        emoticons.put(":-D","smile-big");
        emoticons.put(":(","sad");
        emoticons.put("=(","sad");
        emoticons.put(":-(","sad");
        emoticons.put(":'(","crying");
        emoticons.put(":p","tongue");
        emoticons.put(":P","tongue");
        emoticons.put(":-p","tongue");
        emoticons.put(":-P","tongue");
        emoticons.put(":o","shock");
        emoticons.put("8-0","shock");
        emoticons.put("=8-0","shock");
        emoticons.put(":@","angry");
        emoticons.put(":s","confused");
        emoticons.put(":S","confused");
        emoticons.put(";)","wink");
        emoticons.put(";-)","wink");
        emoticons.put("+o(","sick");
        emoticons.put(":$","embarrassed");
        emoticons.put(":|","disapointed");
        emoticons.put(":-#","shut-mouth");
        emoticons.put("|-)","sleepy");
        emoticons.put("8-)","eyeroll");
        emoticons.put(":\\","thinking");
        emoticons.put(":-\\","thinking");
        emoticons.put("*-)","thinking");
        emoticons.put(":--)","lying");
        emoticons.put("8-|","glasses-nerdy");
        emoticons.put("8o|","teeth");
        emoticons.put("~","excited");
	}
	
}
