from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer


def summarize(text, size=2):
	parser = PlaintextParser.from_string(text, Tokenizer("english"))
	summarizer = LexRankSummarizer()

	summary = summarizer(parser.document, size)
	summarize_text=""
	for sentence in summary:
	    summarize_text+=(str(sentence)+" ")
	    
	summarize_text=summarize_text.strip()
	return summarize_text 
