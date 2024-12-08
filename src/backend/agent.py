from langchain.agents import Tool, AgentExecutor, ZeroShotAgent
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import json

class OrderAgent:
    def __init__(self, database, rag_system):
        self.db = database
        self.rag = rag_system
        self.llm = OpenAI(temperature=0)
        self.tools = self.setup_tools()
        self.agent = self.setup_agent()

    def setup_tools(self):
        return [
            Tool(
                name="Menu Search",
                func=self.search_menu,
                description="Search for menu items and their details"
            ),
            Tool(
                name="Place Order",
                func=self.place_order,
                description="Place a new food order"
            ),
            Tool(
                name="Get Order Status",
                func=self.get_order_status,
                description="Check the status of an order"
            )
        ]

    def setup_agent(self):
        prefix = """You are a helpful restaurant ordering assistant. You can help customers with:
        1. Viewing the menu
        2. Placing orders
        3. Checking order status
        
        Use the tools available to help customers."""
        
        suffix = """Begin!"
        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            self.tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"]
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=self.tools)
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True
        )

    def search_menu(self, query):
        menu_items = self.db.get_menu()
        # Simple search implementation
        query = query.lower()
        matching_items = []
        
        for item in menu_items:
            if (query in item['item_name'].lower() or 
                query in item['description'].lower() or 
                query in item['category'].lower()):
                matching_items.append(item)
        
        return json.dumps(matching_items, indent=2)

    def place_order(self, order_details):
        try:
            order_dict = json.loads(order_details)
            order_id = self.db.place_order(
                order_dict['customer_name'],
                order_dict['items']
            )
            return f"Order placed successfully! Your order ID is: {order_id}"
        except Exception as e:
            return f"Error placing order: {e}"

    def get_order_status(self, order_id):
        try:
            order = self.db.get_order(order_id)
            if order:
                return json.dumps(order, indent=2)
            return "Order not found"
        except Exception as e:
            return f"Error getting order status: {e}"

    def process_message(self, message, chat_history=[]):
        try:
            response = self.agent.run(
                input=message,
                chat_history=chat_history
            )
            return response
        except Exception as e:
            return f"Error processing message: {e}"