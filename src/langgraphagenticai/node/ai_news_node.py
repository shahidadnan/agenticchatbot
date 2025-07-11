from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self,llm):
        self.llm = llm
        self.tavily = TavilyClient()
        """this is used to capture various steps in the file so that later can be use for steps shown"""
        self.state={}
        print("Loaded ai_news_node.py successfully")

    def fetch_news(self, state:dict)->dict:
        """ Fetch Ai news based on specified frequency like [Daily, weekly, Monthly]
            Args:
            state(dict): The state dictionary containing 'frequency'.

            Returns:
                dict: Update state with 'news_data' key containing fetched news.
        """
        frequency = state['messages'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map={'daily':'d', 'weekly':'w','monthly':'m', 'year':'y'}
        days_map={'daily':1, 'weekly': 7, 'monthly':30, 'yearly': 366}

        response = self.tavily.search(
            query="Top Artificial Intelligence(AI) related news India and globally",
            topi="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],
            )
        
        state['news_data']=response.get('results',[])
        self.state['news_data'] = state['news_data']
        return state
        

    def news_summarizer(self, state:dict)->dict:
        """Summarized the news fetched from tavily
        Args:
            state (dict): The state dicitionary conatining 'news_data'.

        returns: 
            dict: Updated state with 'summary' key containing the summarized news.
        """
        news_items = self.state['news_data']
        prompt_template=ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news Article into markdown format. For each items include:
             -Date in **YYY-MM-DD** fromat in IST timezone
             -Concise sentences summary from latest news
             -Sort news by date wise (latest first)
             -source url as link
             Use format:
             ### [Date]
             - [Summary](URL)"""),
             ("user","Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content','')}\nURL: {item.get('url','')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary']=response.content
        self.state['summary']=state['summary']
        return self.state
    

    def save_result(self,state):
        frequency=self.state['frequency']
        summary=self.state['summary']
        filename=f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        
        self.state['filename'] = filename
        return self.state