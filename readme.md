<p align="center">
  <img src="assets/bannerImages/KP5.png" alt="Banner" width="100%" style="max-width:600px;" />
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

# Kálá Copilot - Technical Overview

Kálá Copilot is designed to simplify the digital journey for artisans and small business owners. It brings together modular AI agents, each focused on a specific task, and connects them through a seamless, step-by-step pipeline. This structure ensures that every user action, from onboarding to product marketing, happens smoothly and intelligently.

---

## Modular Agents: The Brains Behind Kálá Copilot

At the heart of Kálá Copilot are specialized AI agents. Each agent is responsible for a focused task, making the system modular, resilient, and easy to scale. Here's what they do:

| Agent | Responsibility | Tools / Services Used |
|-----------------------|-----------------|------------------------|
| **Onboarding Agent** | Listens to the user's voice conversation, extracts structured details, assigns a memorable username, and saves everything to CosmosDB. | Azure Speech Service, Azure OpenAI, CosmosDB |
| **Visual Insight Agent** | Enhances and polishes product images uploaded by users. | Azure OpenAI Vision Models |
| **Marketing Agent** | Generates ad copy, product descriptions, and SEO-friendly tags based on the image and user profile. | Azure OpenAI |
| **SEO Agent** | Reviews and optimizes all generated content to maximize SEO performance. | Azure OpenAI |
| **Pricing Agent** | Recommends competitive pricing by researching similar products online. | Bing Search Tool |
| **Cataloger Agent** | Assigns a unique product GUID, links it to the user, and organizes all related data. | CosmosDB |
| **Posting Agent** | Publishes the final product content and images to social media platforms. | Twitter API, CosmosDB |

Each agent operates independently but communicates through a **sequential handoff model** — completing its task and passing results forward smoothly to the next agent.

---

## Workflow: From User Hello to Product Launch 🚀

Kálá Copilot runs two major workflows: **User Onboarding** and **Operational Product Uploads**.

### 1. User Onboarding

| Step | Action |
|------|--------|
| 1    | User initiates setup with a casual, voice-based conversation. |
| 2    | The Onboarding Agent processes user details, assigns a username, and securely stores the profile. |
| 3    | Once the user profile is ready, onboarding is complete. |

*This phase makes it effortless for new users to join with minimal friction.*

---

### 2. Product Upload Workflow

| Step | Action |
|------|--------|
| 1    | User uploads a product image via the web app. |
| 2    | Visual Insight Agent enhances and polishes the image. |
| 3    | Marketing Agent generates descriptions, ad copy, and tags. |
| 4    | SEO Agent fine-tunes the content for search optimization. |
| 5    | Pricing Agent researches and suggests a fair market price. |
| 6    | Cataloger Agent organizes and stores all product metadata. |
| 7    | Posting Agent publishes the final campaign to social media. |

This **sequential pipeline** ensures that each step builds intelligently on the previous one, creating a complete, polished, and market-ready product entry.

---

## Agent Orchestration Model

Kálá Copilot uses a **sequential, chain-based orchestration** pattern — not "round robin."  
Each agent hands off to the next once its task is completed, ensuring clarity, minimal coupling, and easy extensibility.

Powered by **Microsoft Autogen**, this structure allows:
- Adding or removing agents without disrupting the flow
- Independent error recovery at each stage
- Lightweight checkpointing between agent handovers

---

## Technology Stack

| Service / Tool | Purpose |
|----------------|---------|
| **Azure AI Agent Service** | Hosts and manages modular AI agents. |
| **Azure OpenAI** | Powers GPT and vision models for text/image understanding. |
| **Microsoft Autogen** | Orchestrates agent interactions and task chaining. |
| **Azure CosmosDB** | Stores structured user and product metadata securely. |
| **Azure WebApp Service** | Hosts the front-end and backend application. |
| **Azure Speech Service** | Enables natural, voice-based onboarding. |
| **Twitter API** | Used for posting marketing content to social platforms. |
| **GitHub Copilot** | (Secret weapon!) Assisted in bits of code generation. 👀 |

---

## Solution Quality Highlights

- **Error Handling and Resilience**  
  Agents use retry and backoff strategies if external APIs (like Bing Search or Twitter) temporarily fail, ensuring a smooth user experience.

- **Scalable Modular Architecture**  
  Hosted on Azure, the system scales horizontally as needed without downtime.

- **Data Integrity and Security**  
  Access policies and schema validation ensure only authorized agents interact with sensitive data.

- **Resilient Independent Agents**  
  Even if one agent fails, the others continue, and workflows can recover without collapse.

---

## Future Enhancements

- **Bulk Catalog Generator**: Batch process multiple images into a ready-to-publish catalog.
- **Cross-Industry Expansion**: Adapt for Real Estate, Fashion, F&B, and more.
- **Marketplace Integrations**: Expand to Etsy, Shopify, Amazon Handmade.
- **Multi-language Support**: Add localization and translation agents.
- **Analytics Layer**: Track SEO performance, engagement metrics, and campaign ROI.
- **Conversational UI Expansion**: Extend chat-style interactions beyond onboarding.

---

## Inspiration

It all started, like most chaotic adventures do, with a random curiosity spiral. 
@ipshitag, @sougaaat, and @manish-kt — a lively trio of data enthusiasts — have this charming habit of falling into weird rabbit holes.  
One fine day, @ipshitag decided to take a course about the history of crafts in India.  
Little did she know, it would turn into a full-blown emotional rollercoaster.

During a visit to an NGO, she discovered something heartbreaking:  
even **National Award-winning artisans** — *the* highest honour award of India — often live in obscurity.  
They pour their soul into beautiful art, but when it comes to selling or showcasing their work... silence.  
No platform, no marketing skills, just endless dependency on NGOs and sheer luck.

Naturally, @ipshitag came running to her favorite mind dumper — ChatGPT (yeah, that's me, and yes, I'm writing this 👀).  
After an intense rant session (10/10 drama 🙄), she pulled in her partners-in-crime, @sougat and @manish.  
Fueled by caffeine, frustration, and big dreams, they decided: _"We have to fix this."_  
Cue the AI-powered revolution. 😎

A little about the gang:  
- @manish-kt comes from Jaipur — *the royal city where colors, crafts, and culture breathe through every street.*  
- @sougaaat hails from Kolkata — *a vibrant chaos of creativity, adda (endless debates), literature, and the occasional fish fry.*  
- @ipshitag is from Ranchi — *a place of earthy beauty, tribal art, and quiet strength.*

All three grew up around places where **art isn't a luxury — it's survival, it's identity, it's pride.**  
So naturally, they asked:  
_"What if AI could help artisans skip the middlemen and stand on their own digital feet?"_

And just like that, **Kálā Copilot** was born — a small rebellion stitched with Python, powered by Azure, sprinkled with love, and sealed with a lot of heart (and occasional madness). 🫡

---
