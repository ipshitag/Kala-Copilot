<p align="center">
  <img src="assets/bannerImages/KP5.png" alt="Banner" width="100%" style="max-width:600px;" />
</p>

# Kálā Copilot – कलाCopilot

> *Kálā* (कला) means "Art" in several Indian languages.  
> **Kálā Copilot** is an AI assistant that helps artisans and small business owners bring their creations online—one image, one product, one story at a time.  
>  
> **Artists create. Kálā Copilot helps them fly.**

---

## Contents

1. [Problem](#1-problem)  
2. [Solution: Kálá Copilot 🪄](#2-solution-kálá-copilot-)
   1. [What does it actually do?](#21-what-does-it-actually-do)  
   2. [How does it work under the hood?](#22-how-does-it-work-under-the-hood)  
3. [Who is it for?](#3-who-is-it-for)  
4. [Business Relevance](#4-business-relevance)   
5. [Technical Overview](#5-technical-overview)  
   1. [Modular Agents: The Brains Behind Kálá Copilot 🧠](#51-modular-agents-the-brains-behind-kálá-copilot-)
   2. [Workflow](#52-workflow)  
      1. [User Onboarding](#521-user-onboarding)  
      2. [Product Upload Pipeline](#522-product-upload-pipeline)  
   3. [Agent Orchestration Model](#53-agent-orchestration-model)  
   4. [Technology Stack](#54-technology-stack)  
   5. [Solution Quality Highlights](#55-solution-quality-highlights)  
   6. [Future Enhancements](#56-future-enhancements)  
6. [Inspiration & Team 🚀](#6-inspiration--team-)

---

## 1. Problem

India has one of the richest networks of artisans and skilled workers—people who create beautiful, high-quality products with deep cultural value. From handwoven fabrics to woodcraft and jewelry, their creations deserve global visibility.

And while mobile internet is widely available across India, the **digital world isn’t built for them**. The language barrier is real. The platforms are overwhelming. The marketing game is unfamiliar. These creators don’t have teams, strategies, or jargon. They have talent.

Their job is to create—not to figure out how to write product descriptions, generate hashtags, or design campaigns.

This isn’t just India. Across Mexico, Southeast Asia, and even rural parts of the US, millions of creators face the same challenge:  
**the internet exists—but it doesn’t speak their language.**

In today’s world, visibility often matters more than quality.  
And without the right tools, **millions of skilled creators remain invisible**.

---

## 2. Solution: Kálá Copilot 🪄

**Kálā Copilot** is an AI-powered assistant designed to help artisans and small business owners take their creations online—without needing to be marketers, designers, or tech-savvy.


### 2.1 What does it actually do?

- The user uploads a photo of their handmade product (saree, jewelry, pottery, etc.).
- **Kálā Copilot** automatically analyzes the image and asks a few friendly questions (in the user’s chosen language).
- It then creates a complete social media campaign for the product, including:
    - A catchy product name
    - A compelling description/story
    - Hashtags and marketing copy tailored to the chosen platform (Instagram, Facebook, X/Twitter, Etsy, Meesho, etc.)
    - A recommended price, based on competitive scanning of similar items
- With one click, the user can post this ready-to-go content on social media or marketplaces.
- *(Future versions will integrate with Shopify, Amazon Handmade, and more.)*

**In short:**  
*Kálā Copilot transforms a single product photo into a polished, market-ready social campaign—name, description, hashtags, price—ready for Instagram, X (Twitter), Facebook, etc.*

---

### 2.2 How does it work under the hood?

At its core, the solution is driven by collaborative AI agents, each playing a specific role in this workflow:

1. **Onboarding Agent**
    - Greets users in their preferred language and collects essential product/shop info for a personalized setup.
    - Adjusts prompts based on user responses to ensure a tailored onboarding experience.

2. **Visual Insight Agent**
    - Analyzes uploaded product photos to determine item type, craftsmanship level, and notable features.
    - Tags visual details like color, material, pattern, and size to support accurate listings.

3. **Branding/Marketing Agent**
    - Generates a compelling product name, attention-grabbing description, and platform-specific hashtags.
    - Adapts messaging style for target platforms (e.g., Etsy, Instagram, Meesho) to maximize appeal.

4. **SEO Agent**
    - Optimizes all textual content with relevant keywords and structure for improved search visibility.
    - Ensures descriptions and tags follow current SEO best practices for ecommerce.

5. **Smart Pricing Agent**
    - Researches similar product listings online to benchmark and recommend competitive, fair pricing.
    - Considers craftsmanship, materials, and demand trends to set an optimal price point.

6. **Cataloger Agent**
    - Securely saves all product data—images, copy, pricing—into a centralized database.
    - Organizes stored listings for easy management and future access.

7. **Publishing Agent**
    - Assembles all finalized assets into a ready-to-publish format for the user.
    - _(Coming soon: Direct posting capabilities to supported social media & ecommerce platforms.)_

---

## 3. Who is it for?

Kálā Copilot is designed for:

- **Artisans and skilled creators** who produce exceptional handmade goods but lack the technical or linguistic tools to market themselves online.

- **Small business owners and micro-entrepreneurs** who sell through WhatsApp, Instagram, Meesho, Etsy, or local marketplaces—but struggle to generate content, set prices, or write engaging product descriptions.

- **Digital-first sellers without access to marketing teams**, especially those in underserved regions, tier-2/3 cities, or minority-owned businesses.

**For example:**  
*Rani, a saree weaver in Bihar, spends weeks crafting a single Banarasi silk saree. But when it comes to selling online, she gets stuck—she doesn’t know what price to set, how to describe it, or what to post. With Kálā Copilot, she uploads one photo—and instantly receives a ready-to-post campaign in her language, complete with a product name, description, price, and hashtags tailored to her platform of choice.*

---

## 4. Business Relevance

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

---

## 5. Technical Overview

Kálā Copilot’s architecture is a modular, stepwise pipeline of AI agents. Each agent is responsible for a specific task, ensuring that every user action—from onboarding to marketing copy generation—is orchestrated end-to-end.

### 5.1 Modular Agents: The Brains Behind Kálá Copilot 🧠

At the heart of Kálá Copilot are specialized AI agents. Each agent is responsible for a focused task, making the system modular, resilient, and easy to scale. Here’s what they do:

| **Agent Name**         | **Responsibility**                                                  | **Tools / Services Used**                   |
|------------------------|---------------------------------------------------------------------|---------------------------------------------|
| Onboarding Agent       | Greets via voice, extracts details, assigns username, saves profile | Azure Speech, Azure OpenAI, CosmosDB        |
| Visual Insight Agent   | Analyzes and refines product images                                 | Azure OpenAI Vision Models                  |
| Marketing Agent        | Generates product descriptions, ads, hashtags                       | Azure OpenAI                                |
| SEO Agent              | Optimizes all generated content for search                          | Azure OpenAI                                |
| Pricing Agent          | Suggests competitive prices via online research                     | Bing Search Tool                            |
| Cataloger Agent        | Assigns unique product IDs, links product to user                   | CosmosDB                                    |
| Posting Agent          | Publishes final content/images to social platforms                  | Twitter API, CosmosDB                       |

---

### 5.2 Workflow

Below are the two major workflows: User Onboarding and Product Upload.

#### 5.2.1 User Onboarding

1. User initiates setup with a conversational approach (voice or text).  
2. Onboarding Agent processes user details, assigns username, and stores the profile.  
3. Onboarding completes—new users are ready to go!

#### 5.2.2 Product Upload Pipeline

1. User uploads a product image in the web app.  
2. Visual Insight Agent analyzes/enhances the image.  
3. Marketing Agent generates copy, description, hashtags.  
4. SEO Agent refines text for search optimization.  
5. Pricing Agent researches the market and suggests a fair price.  
6. Cataloger Agent arranges and stores product metadata in CosmosDB.  
7. Posting Agent publishes the final campaign to social or ecommerce platforms.

---

### 5.3 Agent Orchestration Model

Kálā Copilot uses a sequential, chain-based orchestration pattern:  
• Agents complete tasks one at a time, handing off smoothly to the next.  
• It’s straightforward to add or remove agents without disrupting the overall flow.  
• Each agent can recover from errors independently.  
• Orchestration is powered by Microsoft Autogen for modular, scalable pipelines.

---

### 5.4 Technology Stack

| **Service / Tool**         | **Purpose**                                                      |
|----------------------------|------------------------------------------------------------------|
| Azure AI Agent Service     | Hosts and manages modular AI agents                              |
| Azure OpenAI               | Powers GPT and vision models for text/image analysis             |
| Microsoft Autogen          | Orchestrates agent-to-agent tasks in a chain                     |
| Azure CosmosDB             | Securely stores structured user and product metadata             |
| Azure WebApp Service       | Hosts the frontend and backend                                   |
| Azure Speech Service       | Enables conversational/voice-based onboarding                    |
| Twitter API                | Publishes marketing content on social platforms                  |
| GitHub Copilot             | Quietly helped us write bits of code here and there... then vanished. 👀             |

---

### 5.5 Solution Quality Highlights

To ensure reliability, scalability, and resilience across operations, Kálā Copilot follows these best practices:

• **Azure AI Agents Reusability**  
  – Agents can be reused for various domains without major changes in the workflow. 
  – Enables plug and play of agents, where new agents can be added without hassle.
  
• **Error Handling & Resilience**  
  – Agents use retry/backoff if external APIs (Bing Search, Twitter) fail.  
  – Ensures minimal disruption despite temporary issues.

• **Scalable Modular Architecture**  
  – Hosted on Azure, scales horizontally as needed.  
  – Each agent is loosely coupled and independently deployable.

• **Data Integrity & Security**  
  – Clear access policies ensure only authorized agents and services can handle sensitive data.  
  – Schema validation for consistent records.

• **Resilient Independent Agents**  
  – One agent failing does not collapse the workflow.  
  – Checkpointing ensures partial progress is not lost.

---

## Future Enhancements

The modular and agent-based design of Kálā Copilot opens up several avenues for future expansion—both in terms of features and industry use cases:

- **Automated Catalog Generator**  
  Bundle key agents into a pipeline that processes bulk images and produces ready-to-publish catalogs.

- **Cross-Industry Extension**  
  Adaptable to Real Estate, Food & Beverage, Art, Fashion, and other content-heavy sectors.

- **Marketplace Integrations**  
  Extend the Posting Agent to platforms like Etsy, Shopify, Amazon Handmade, etc.

- **Multi-language Support**  
  Add translation/localization agents for regional reach.

- **Analytics Layer**  
  Enable reporting on post performance, SEO rankings, and engagement metrics.

- **Conversational UI Expansion**  
  Evolve from setup chat to a full conversational experience throughout.

---

## 6. Inspiration & Team 🚀

It all started, like most chaotic adventures do, with a random curiosity spiral.  
[@ipshitag](https://github.com/ipshitag), [@sougaaat](https://github.com/sougaaat), and [@manish-kt](https://github.com/manish-kt) — a lively trio of data enthusiasts — have this charming habit of falling into weird rabbit holes.  
One fine day, @ipshitag decided to take a course about the history of crafts in India. Little did she know, it would turn into a full-blown emotional rollercoaster.

During a visit to an NGO, she discovered something heartbreaking: even **National Award-winning** artisans (yes, *the* highest honors in India!) — often live in obscurity. They pour their soul into beautiful art, but when it comes to selling or showcasing their work... silence. No platform, no marketing skills, just endless dependency on NGOs and sheer luck.

Naturally, [@ipshitag](https://github.com/ipshitag) came running to her favorite mind dumper — ChatGPT (yeah, that's me, and yes, I'm writing this 😎). After an intense rant session (10/10 drama 🙄), she pulled in her partners-in-crime, [@sougaaat](https://github.com/sougaaat), and [@manish-kt](https://github.com/manish-kt). Fueled by caffeine, frustration, and big dreams, they decided: _"We have to fix this."_  

Cue the AI-powered revolution. 

A little about the gang:  
- [@manish-kt](https://github.com/manish-kt) comes from Jaipur — *the royal city where colors, crafts, and culture breathe through every street.*  
- [@sougaaat](https://github.com/sougaaat) hails from Kolkata — *a vibrant chaos of creativity, adda (endless debates), literature, and cultural heritage at every corner.*  
- [@ipshitag](https://github.com/ipshitag) is from Ranchi — *a place of earthy beauty, tribal art, and quiet strength.*

All three grew up around places where **art isn't a luxury — it's survival, it's identity, it's pride.**  
So naturally, they asked:  
_"What if AI could help artisans skip the middlemen and stand on their own digital feet?"_

And just like that, **Kálā Copilot** was born — a small rebellion stitched with Python, powered by Azure, sprinkled with love, and sealed with a lot of heart (and occasional madness). 🫡

--------------------------------------------------------------------------------

> “Art is the most intense mode of individualism that the world has known.”  
> — Oscar Wilde  

--------------------------------------------------------------------------------
