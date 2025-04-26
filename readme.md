<p align="center">
  <img src="https://github.com/ipshitag/Retail-Copilot-Hackathon/blob/main/assets%2FbannerImages%2FKP5.png" alt="Banner" width="100%" style="max-width:600px;" />
</p>

# कलाCopilot – Kálā Copilot
> *Kálā* (कला) means "Art" in several Indian languages.  
> **Kálā Copilot** is an AI-powered assistant that helps artisans and small business owners bring their creations online—one image, one product, one story at a time.  
>  
> **Artists create. Kálā Copilot helps them fly.**
---

## **1. Problem**

India has one of the richest networks of artisans and skilled workers—people who create beautiful, high-quality products with deep cultural value. From handwoven fabrics to woodcraft and jewelry, their creations deserve global visibility.

And while mobile internet is widely available across India, the **digital world isn’t built for them**. The language barrier is real. The platforms are overwhelming. The marketing game is unfamiliar. These creators don’t have teams, strategies, or jargon. They have talent.

Their job is to create—not to figure out how to write product descriptions, generate hashtags, or design campaigns.

This isn’t just India. Across Mexico, Southeast Asia, and even rural parts of the US, millions of creators face the same challenge:  
**the internet exists—but it doesn’t speak their language.**

In today’s world, visibility often matters more than quality.  
And without the right tools, **millions of skilled creators remain invisible**.

---

## **2. Solution: Kálā Copilot**

**Kálā Copilot** is an AI-powered assistant designed to help artisans and small business owners take their creations online—without needing to be marketers, designers, or tech-savvy.

At its core, the solution is driven by **five collaborative AI agents**, each playing a specific role:

### 1. **Onboarding Agent**  
The first interaction starts with a conversational agent that “speaks” with the user in their preferred language—asking for basic info like product category, materials used, shop name, and any past listings. This ensures a personalized and localized experience from the start.

### 2. **Visual Insight Agent**  
Once the user uploads a product photo, this agent analyzes the image to:
- Identify the object (e.g., handcrafted bag, ceramic bowl, saree)  
- Gauge the quality, size, texture, and level of craftsmanship  
- Tag relevant features like color, pattern, and utility  

### 3. **Branding Agent**  
This agent generates complete campaign-ready content:
- A compelling **product name**  
- A catchy **tagline**  
- A platform-appropriate **description** with relevant hashtags  
It adapts tone and language for different platforms like Meesho, Instagram, Etsy, etc.

### 4. **Smart Pricing Agent**  
To determine the right price, this agent scans similar products across the internet—including ecommerce platforms, local seller listings, and platform-specific trends. It balances market rates with craftsmanship to recommend a fair, competitive price.

### 5. **Publishing Agent**  
Finally, this agent compiles the output and provides ready-to-paste captions and content for the user's platform of choice. Future iterations will include direct posting integrations.

---

## **3. Who is it for?**

Kálā Copilot is designed for:

- **Artisans and skilled creators** who produce exceptional handmade goods but lack the technical or linguistic tools to market themselves online.

- **Small business owners and micro-entrepreneurs** who sell through WhatsApp, Instagram, Meesho, Etsy, or local marketplaces—but struggle to generate content, set prices, or write engaging product descriptions.

- **Digital-first sellers without access to marketing teams**, especially those in underserved regions, tier-2/3 cities, or minority-owned businesses.

**For example:**  
*Rani, a saree weaver in Bihar, spends weeks crafting a single Banarasi silk saree. But when it comes to selling online, she gets stuck—she doesn’t know what price to set, how to describe it, or what to post. With Kálā Copilot, she uploads one photo—and instantly receives a ready-to-post campaign in her language, complete with a product name, description, price, and hashtags tailored to her platform of choice.*

---

## **4. Business Relevance**

Kálā Copilot isn’t just a tool—it’s a business enabler.

By lowering the barrier to online selling, it unlocks a massive user base that has so far been underserved by the digital economy. These creators and micro-entrepreneurs represent a **huge untapped market** for ecommerce platforms, social commerce apps, and logistics players.

### Why it matters:
- **Enables platforms like Meesho, Flipkart, or Amazon India** to onboard thousands of new sellers with ready-to-use listings  
- **Creates direct value for marketplaces** by improving listing quality, discoverability, and product data structure  
- **Bridges the creator-to-customer gap**, especially in regions where marketing talent or English fluency is limited  
- **Adds multilingual and culturally localized content**, expanding reach across languages and markets  
- Can be extended to global marketplaces like **Etsy, eBay, or Meta Shops**, giving artisans from India, Mexico, and beyond the tools to go global

Kálā Copilot turns individual creators into micro-brands—without requiring them to learn marketing.  
And for platforms, it boosts growth at scale, one creator at a time.

# Kálā Copilot — Technical Documentation

## Overview

Kálā Copilot is a modular AI-powered pipeline built using Microsoft Autogen and Azure’s AI Agent Service. It helps artisans convert raw product ideas into high-quality marketing material and catalog-ready listings—entirely through automation.

The system is orchestrated through a sequence of intelligent agents that handle different stages of product onboarding, enhancement, and publishing. Each agent performs its task and passes the result to the next in a **RoundRobin** manner.

---

## Agent Workflow

Each agent is orchestrated via Microsoft **Autogen**, connected in a RoundRobin fashion where outputs flow into the next agent. The order of execution is:

| Agent Name         | Description |
|--------------------|-------------|
| **Onboarding Agent** | Processes voice-based onboarding conversations. Extracts user info, generates memorable usernames, and stores structured user profiles in CosmosDB. Also includes CosmosDB tools for direct storage. |
| **Visual Insight Agent** | Enhances and analyzes uploaded product images. Generates a clean, high-quality version optimized for listings. |
| **Marketing Agent** | Takes image analysis + user data to generate product descriptions, social captions, hashtags, and marketing copy. |
| **SEO Agent** | Reviews and improves the generated ad copy to optimize it for search engines. |
| **Pricing Agent** | Scrapes pricing information using Bing tools and suggests an optimal price based on market trends and product attributes. |
| **Cataloger Agent** | Saves the finalized product listing to CosmosDB with a unique GUID and user ID key. Uses CosmosDB tools for structured storage. |
| **Posting Agent** | Fetches listing from CosmosDB and posts to social platforms using APIs (e.g., Twitter API). |

---

## Agent Orchestration: RoundRobin Style

The agents follow a **RoundRobin orchestration pattern** using Microsoft Autogen. Each agent performs its task and passes the result to the next in line, forming a linear and modular pipeline. This ensures clarity, low coupling between agents, and allows new agents to be inserted or removed without disrupting the overall flow.

> This approach enhances scalability and modular innovation—agents are plug-and-play, making it easy to experiment with new logic or repurpose the flow for different industries and datasets.

---

## Stack and Resources Used

| Resource | Purpose |
|----------|---------|
| **Azure AI Agent Service** | Hosts the orchestration and manages agent communication. |
| **Azure OpenAI** | Powers the core intelligence behind most agents (e.g., onboarding, marketing). |
| **Microsoft Autogen** | Enables dynamic multi-agent conversations in a RoundRobin chain. |
| **Azure CosmosDB** | Stores structured product and user data. Enables fast reads/writes. |
| **Azure WebApp Service** | Hosts the frontend experience for users. |
| **Azure Speech Service** | Converts voice onboarding into text for analysis. |
| **Twitter API** | Used by the Posting Agent to publish product listings to social media. |
| **GitHub Copilot** | Helped us sneakily write some of the logic across agents and utilities here and there 👀 |

---

## Design Highlights

- **Low-Code Modularity**: Each agent is designed as a standalone service, easily replaceable or extendable without touching the core orchestration logic.
- **Python-Native Stack**: Built entirely using Python-first tools like Azure Autogen, OpenAI SDKs, and CosmosDB clients.
- **Optimized for Ease**: The user interface is minimal and voice-led; product listing is reduced to an image upload with zero technical friction.
- **Infra Efficiency**: Azure services ensure serverless scale, reliability, and minimal devops overhead.

---

## Operational Flow

### Onboarding Phase
1. User sets up their account via a **voice-based conversation**, where they naturally provide all needed information.
2. This information is passed to the **Onboarding Agent**, which parses and stores the details in CosmosDB.
3. Onboarding completes with user data structured and accessible.

### Product Listing Phase
1. User uploads an image.
2. It goes through the following pipeline:
   - **Visual Insight Agent**
   - **Marketing Agent**
   - **SEO Agent**
   - **Pricing Agent**
   - **Cataloger Agent**
   - **Posting Agent**

Each agent contributes to improving, enriching, and finalizing the product listing before it is published online.

---

## Future Enhancements

- **Multi-industry Extensions**: The agent pipeline can be adapted to other domains like food, real estate, fashion, etc.
- **Bulk Catalog Mode**: Upload a folder of images to generate a fully detailed product catalog automatically.
- **E-commerce Sync**: Push finalized products directly into Shopify, Etsy, or custom storefronts.
- **Language Support**: Extend multilingual onboarding and generation beyond English for regional users.

---