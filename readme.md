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
2. [Solution: Kálā Copilot](#2-solution-kálā-copilot)
   1. [How does it work under the hood?](21-how-does-it-work-under-the-hood)  
4. [Who is it for?](#3-who-is-it-for)  
5. [Business Relevance](#4-business-relevance)  
6. [Technical Overview](#5-technical-overview)
   1. [Why AI Agents?](#why-ai-agents)  
   2. [Modular Agents: The Brains Behind Kálā Copilot](#51-modular-agents-the-brains-behind-kálā-copilot)
   3. [Workflow](#52-workflow)  
      1. [User Onboarding](#521-user-onboarding)  
      2. [Product Upload Pipeline](#522-product-upload-pipeline)  
   3. [Agent Orchestration Model](#53-agent-orchestration-model)  
   4. [Technology Stack](#54-technology-stack)  
   5. [Solution Quality Highlights](#55-solution-quality-highlights)  
   6. [Future Enhancements](#56-future-enhancements)  
7. [Inspiration & Team 🚀](#6-inspiration--team-)

---

## 1. Problem

Millions of skilled creators around the world—artisans, craftspeople, small makers—are invisible in the digital economy.

Not because they lack talent.  
Because the internet wasn’t built for them.

Platforms are complex. Marketing is a second language.  
They don't have content teams or ad budgets. They have skill, history, and product.

Today, **visibility beats quality**.  
And without the right tools, these creators get left out of the global marketplace.

This isn’t just an India problem. It's global—from Southeast Asia to Latin America to rural U.S. towns.  
**The internet exists—but it doesn’t speak their language.**

There’s a massive opportunity to unlock creativity, culture, and commerce—at scale—by building tools *for* them, not *against* them.

---

## 2. Solution: Kálā Copilot
**Kálā Copilot** is an AI-powered assistant designed to help artisans and small business owners take their creations online—without needing to be marketers, designers, or tech-savvy. Following is an ideal workflow:

- The artisan (or small business owner) uploads a product photo (saree, jewelry, pottery, etc.).  
- Kálā Copilot analyzes the image, asks a few friendly questions in the user’s chosen language, and then:  
  - Generates a catchy product name  
  - Crafts a compelling product description/story  
  - Suggests relevant hashtags/marketing copy for platforms like Instagram, Facebook, X (Twitter), Etsy, Meesho, etc.  
  - Recommends a competitive price  
- The user can then post the ready-made content directly to their social media or marketplace.  
- *(Future versions will expand integrations to Shopify, Amazon Handmade, and more!)*

In short:  
**Kálā Copilot** transforms a single product photo into a polished social media campaign—complete with name, description, hashtags, and price—all set to launch with one click.

---

### 2.1 How does it work under the hood?
At its core, the solution is driven by **seven collaborative AI agents**, each playing a specific role:

1. **Onboarding Agent**  
   - Welcomes users in their preferred language and captures general shop/product info.  
   - Tailors prompts for a personalized experience.

2. **Visual Insight Agent**  
   - Examines product photos for color, material, patterns, etc.  
   - Provides refined tags for accurate listings.

3. **Branding/Marketing Agent**  
   - Creates product names, marketing messages, descriptions, and hashtags.  
   - Adapts style to each platform (e.g., Etsy, Instagram, Meesho).

4. **SEO Agent**  
   - Infuses relevant keywords for better search visibility.  
   - Ensures best practices for ecommerce SEO are followed.

5. **Smart Pricing Agent**  
   - Searches similar listings to propose a fair, competitive price.  
   - Considers craftsmanship, demand, materials, and historical data.

6. **Cataloger Agent**  
   - Saves all product data securely, assigning unique product IDs.  
   - Maintains an organized database for quick retrieval.

7. **Publishing Agent**  
   - Assembles finalized content (photos, name, description) for posting.  
   - (Coming soon: Direct auto-posts to various platforms.)

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

### 4.1 Why it matters:
 - **Enables platforms like Meesho, Flipkart, or Amazon India** to onboard thousands of new sellers with ready-to-use listings  
 - **Creates direct value for marketplaces** by improving listing quality, discoverability, and product data structure  
 - **Bridges the creator-to-customer gap**, especially in regions where marketing talent or English fluency is limited  
 - **Adds multilingual and culturally localized content**, expanding reach across languages and markets  
 - Can be extended to global marketplaces like **Etsy, eBay, or Meta Shops**, giving artisans from India, Mexico, and beyond the tools to go global
 
 Kálā Copilot turns individual creators into micro-brands—without requiring them to learn marketing.  
 And for platforms, it boosts growth at scale, one creator at a time.

---

## 5. Technical Overview
In this section, we outline the modular architecture that powers Kálā Copilot. Our system employs a chain-of-agents approach, ensuring each AI agent focuses on a specific task.

But first, let's answer an important question: **Why AI agents, and not just a single large model or a traditional app?**

### Why AI Agents?

Kálā Copilot leverages **AI agents** to create a natural, human-friendly experience for artisans and small business owners who are not familiar with complex digital systems.

Each agent is **autonomous**, meaning it specializes in a specific task—such as onboarding, visual analysis, branding, SEO optimization, or pricing—and can independently perceive user inputs, make decisions, and take actions based on its role. The agents collaborate through an orchestration layer (Microsoft Autogen) to complete complex workflows seamlessly.

Instead of forcing users to fill out rigid forms or follow strict templates, Kálā Copilot agents **extract structured information** (like product details, pricing suggestions, hashtags, and descriptions) directly from **unstructured, natural inputs**—whether that’s a photo, a voice message, or casual text.

Additionally, using **Azure AI Agents** makes the architecture highly modular and scalable. Each agent is **plug-and-play** — meaning new capabilities (e.g., real estate listings, restaurant menus, fashion styling) can be added simply by creating or swapping agents, without rewriting the core system.  
This **reusability** ensures that Kálā Copilot can evolve into a multi-industry solution without major redevelopment.

This approach ensures:
- **Flexibility**: Users can interact naturally without needing technical knowledge.
- **Accuracy**: Specialized agents handle tasks with domain-specific intelligence.
- **Scalability**: New agents or industries can be added through plug-and-play extension.
- **Resilience**: Individual agent failures do not crash the entire workflow.

In short:  
> **Instead of making users think like machines, we made machines think like users.**

### Architecture Diagram
<p align="center">
  <img src="https://github.com/ipshitag/Retail-Copilot-Hackathon/blob/main/assets/ReadmeImages/Architecture_KalaCopilot.png" 
       alt="Kala Copilot Architecture Diagram" 
       width="100%" />
</p>


### 5.1 Modular Agents: The Brains Behind Kálā Copilot
Here’s a quick snapshot of the specialized agents:

| **Agent Name**         | **Responsibility**                                                  | **Tools / Services Used**      |
|------------------------|---------------------------------------------------------------------|--------------------------------|
| Onboarding Agent       | Welcomes user, captures details, stores profile                     | Azure Speech, OpenAI, CosmosDB |
| Visual Insight Agent   | Analyzes product images                                             | Azure OpenAI Vision            |
| Marketing Agent        | Generates copy, ads, hashtags                                       | Azure OpenAI                   |
| SEO Agent              | Optimizes text for relevant searches                                | Azure OpenAI                   |
| Pricing Agent          | Recommends fair, market-aligned prices                              | Bing Search Tool               |
| Cataloger Agent        | Stores product data in CosmosDB                                     | CosmosDB                       |
| Posting Agent          | Publishes final content                                             | Twitter API, CosmosDB          |

---

### 5.2 Workflow
The system operates in two main phases: **User Onboarding** and **Operational Workflow**, orchestrated using **Microsoft Autogen** with a RoundRobin-style conversation pattern between agents.

#### 5.2.1 User Onboarding
1. The user begins a conversational setup (voice or text).  
2. Onboarding Agent processes user details, assigns a username, and saves profile info in CosmosDB.  
3. User is ready to proceed—no marketing experience needed!

#### 5.2.2 Product Upload Pipeline
1. The user uploads a product image.  
2. Visual Insight Agent refines image data.  
3. Marketing Agent drafts the product name, description, and hashtags.  
4. SEO Agent applies search-friendly keywords.  
5. Pricing Agent checks competitor data to suggest pricing.  
6. Cataloger Agent organizes and secures all final product info.  
7. Posting Agent compiles everything for a frictionless publish.

---

### 5.3 Agent Orchestration Model
Kálā Copilot uses a **chain-based orchestration** where agents process tasks in sequence:
- Each agent passes data to the next, ensuring simple handoffs.  
- Modular design allows adding/removing agents without breaking the entire flow.  
- Each agent can handle errors and retry independently.  
- Orchestration is managed by Microsoft Autogen, supporting flexible, scalable agent pipelines.

<p align="center">
  <img src="https://github.com/ipshitag/Retail-Copilot-Hackathon/blob/main/assets/bannerImages/agent-workflow.png" 
       alt="Agent workflow diagram" 
       width="300" />
</p>

---

### 5.4 Technology Stack
| **Service / Tool**         | **Purpose**                                             |
|----------------------------|---------------------------------------------------------|
| Azure AI Agent Service     | Manages modular AI agents                               |
| Azure OpenAI               | GPT & vision models for analysis                        |
| Microsoft Autogen          | Orchestrates agent tasks                                |
| Azure CosmosDB             | Stores user/product data securely                      |
| Azure WebApp Service       | Hosts the frontend/backend                              |
| Azure Speech Service       | Enables voice-based onboarding                          |
| Azure Storage              | Saves uploaded data                                     |
| Twitter API                | Publishes marketing content                             |
| GitHub Copilot             | Some help here and there  👀 |

---

### 5.5 Solution Quality Highlights
Below are some key highlights that ensure solution quality:  
- **Modular Reusability**  
  Each agent can be repurposed across industries or different product lines with minor tweaks.  
- **Error Handling & Resilience**  
  Agents retry or use fallback if external APIs fail. Minimizes disruptions.  
- **Scalable Architecture**  
  Deployed on Azure; horizontal scaling is straightforward.  
- **Data Security**  
  Strict access policies and schema validation ensure only authorized processes handle sensitive data.  
- **Resilient Independent Agents**  
  A failure in one area doesn’t derail the entire workflow.

---

### 5.6 Future Enhancements
Potential future enhancements are described below:

<details>
<summary>Click to expand Future Enhancements</summary>

- **Automated Catalog Generator**  
  Bulk process multiple images for ready-to-publish product catalogs.

- **Multi-Industry Extension**  
  Adapt this model to Real Estate, Food & Beverage menus, Art portfolios, and more.

- **Marketplace Integrations**  
  Expand direct publishing to Shopify, Amazon Handmade, Etsy, etc.

- **Multilingual Localizations**  
  Additional languages via translation agents for global coverage.

- **Analytics & Reporting**  
  Track post-performance, SEO metrics, user engagement, and sales conversions.

- **Deeper Conversational UI**  
  Evolve from simple onboarding chat to a fully conversational experience for all steps.
</details>

---

## 6. Inspiration & Team 🚀
<details>
<summary>Click to learn about our journey</summary>

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

> “Art is the most intense mode of individualism that the world has known.”  
> — Oscar Wilde  
</details>

---
