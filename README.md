# Gemini Pro LINE Bot on Cloud Function with Firebase Database

This project demonstrates how to create a LINEBot with memory capabilities, allowing for continuous and context-aware conversations. The bot leverages several platforms for its development and deployment.

       ┌─┐                                                                                       
       ║"│                                                                                       
       └┬┘                                                                                       
       ┌┼┐                                                                                       
        │            ┌─────┐          ┌──────────────┐               ┌────────┐          ┌──────┐
       ┌┴┐           │Group│          │Webhook_Server│               │Firebase│          │Gemini│
      User           └─────┘          └──────┬───────┘               └────────┘          └──────┘
       │    傳送文章訊息  │                    │                           │                  │    
       │ ──────────────>│                    │                           │                  │    
       │                │                    │                           │                  │    
       │                │     傳送用戶指令     │                           │                  │    
       │                │───────────────────>│                           │                  │    
       │                │                    │                           │                  │    
       │                │                    │   儲存聊天狀態在 Realtime DB│                  │    
       │                │                    │ ────────────────────────> |                 │    
       │                │                    │                           │                  │    
       │                │                    │           儲存完畢         │                  │    
       │                │                    │ <──────────────────────── |                  │    
       │                │                    │                           │                  │    
       │                │    回傳已完成文字    │                           │                  │    
       │                │<───────────────────│                           │                  │    
       │                │                    │                           │                  │    
       │   輸入 "!摘要"  │                    │                           │                  │    
       │ ──────────────>│                    │                           │                  │    
       │                │                    │                           │                  │    
       │                │     傳送用戶指令     │                           │                  │    
       │                │───────────────────>│                           │                  │    
       │                │                    │                           │                  │    
       │                │                    │          抓取聊天記錄       │                  │    
       │                │                    │ ────────────────────────> |                  │    
       │                │                    │                           │                  │    
       │                │                    │           回傳清單         │                  │    
       │                │                    │ <─────────────────────────|                  │    
       │                │                    │                           │                  │    
       │                │                    │               下prompt 進行摘要運算            │    
       │                │                    │ ────────────────────────────────────────────>|    
       │                │                    │                           │                  │    
       │                │                    │                   回傳摘要清單                 │    
       │                │                    │ <────────────────────────────────────────────|    
       │                │                    │                           │                  │    
       │                │   回傳摘要資訊至群組  │                           │                  │    
       │                │<───────────────────│                           │                  │    
      User           ┌─────┐          ┌──────┴───────┐               ┌────────┐          ┌──────┐
       ┌─┐           │Group│          │Webhook_Server│               │Firebase│          │Gemini│
       ║"│           └─────┘          └──────────────┘               └────────┘          └──────┘
       └┬┘                                                                                       
       ┌┼┐                                                                                       
        │                                                                                        
       ┌┴┐                                                                                       

## Platforms Used

- **LINE Developers**: To create and configure the LINEBot.
- **Gemini Pro**: To enable conversational AI capabilities.
- **Google Cloud Functions**: To deploy the Python code and generate a webhook for the LINEBot.
- **Firebase**: To establish a real-time database for storing conversation history.

## LINEBot Creation

### Step 1: Create a Bot on LINE Developers

### Step 2: Configure Bot Basic Information

- **Channel type**: Set to Messaging API (mandatory).
- **Provider**: Use an existing one or create a new one if you haven't used it before.
- **Other options**: Fill in the details as required.
- **Bot profile image**: Upload a custom image.
- **Privacy policy URL, Terms of use URL**: These can be left blank.

### Step 3: Obtain Bot's Channel Secret and Channel Access Token

After creating the bot, find the Channel secret on the Basic Setting page and the Channel access token on the Messaging API page. These will be used in the code.

**Note**: If you issue or reissue these credentials, remember to update them in your code.

### Step 4: Finalize Bot Setup

Set aside the bot for now. Once the program is deployed, paste the URL back into the Webhook URL field on the Messaging API page.

## Gemini Pro API

Refer to the official Gemini Pro website and tutorials for guidance. Remember to save your API Keys securely as they can only be copied at the time of creation.

## Firebase

### Step 1: Get Started

Click on 'Get Started'.

### Step 2: Create a Project

Click on 'Add Project' and make sure to enable Google Analytics.

### Step 3: Enter Realtime Database

After entering Realtime Database, create a new database in locked mode and then modify it.

Once you see a URL like `https://XXX.firebaseio.com/`, that's the URL you'll use in the program to set the data storage location.

### Step 4: Change Rules

In the 'Rules' section, change `false` to `true` to allow external writes.

## Google Cloud Functions

### Step 0: Introduction to Google Cloud

Google Cloud offers a suite of cloud computing services, including computing, data storage, data analytics, and machine learning.

### Step 1: Get Started

Click on 'Console' or 'Start a Free Trial' on the website.

### Step 2: Create a Project in Cloud Functions

Find Cloud Functions in the menu or under the 'Serverless' category.

### Step 3: Create a Function

Set the environment to the first generation and the region to `asia-east1` (Taiwan). Set the trigger to HTTP and allow unauthenticated invocations.

Add four runtime environment variables:

- `GOOGLE_GEMINI_API_KEY`: Your Gemini Pro secret key.
- `ChannelAccessToken`: Your LINE Developers Channel access token.
- `ChannelSecret`: Your LINE Developers Channel secret.
- `FIREBASE_URL`: Your Firebase URL.

### Step 4: Deploy

After setting up the function, deploy it. Once deployed, you'll find a 'Trigger URL' that you'll paste back into your LINEBot.

## Result

You can check the conversation history stored in Firebase.

With this setup, you have successfully created a LINEBot with memory capabilities, allowing for more engaging and contextually aware conversations.
# chatbot-culture
# chatbot-culture
# chatbot-culture
# chatbot-culture
# chatbot-culture
