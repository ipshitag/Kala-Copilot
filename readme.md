<!-- 
  HACKATHON-FRIENDLY README WITH IMPROVED FORMATTING, COLLAPSIBLE SECTIONS, 
  CONSISTENT HEADING STRUCTURE, AND LIGHT EMOJIS
  Audience: Hackathon Judges
-->

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
2. [Solution: Kálā Copilot 🪄](#2-solution-kálā-copilot-)  
   1. [What does it actually do?](#21-what-does-it-actually-do)  
   2. [How does it work under the hood?](#22-how-does-it-work-under-the-hood)  
3. [Who is it for?](#3-who-is-it-for)  
4. [Business Relevance](#4-business-relevance)  
5. [Technical Overview](#5-technical-overview)  
   1. [Modular Agents: The Brains Behind Kálā Copilot 🧠](#51-modular-agents-the-brains-behind-kálā-copilot-)
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
In many parts of the world, highly skilled artisans create stunning products with immense cultural value. However, they often remain invisible online. Why? Because platforms are complicated, language barriers exist, and digital marketing isn’t second nature to them.

<p align="center">
  <img src="https://github.com/ipshitag/Retail-Copilot-Hackathon/blob/main/assets/bannerImages/PunjabiPhulkari.png" 
       alt="Group of Punjabi women practicing phulkari embroidery" 
       width="60%" style="max-width:450px;" />
</p>

India, for instance, has a vast network of talented weavers, jewelers, and craftsmen. Yet they lack the technical or linguistic resources to effectively market their art. This phenomenon repeats in Mexico, Southeast Asia, and even parts of the U.S.

In our increasingly digital world, visibility can matter more than quality.  
Without the right tools, millions of artisans—and their incredible products—remain hidden from global audiences.

---

## 2. Solution: Kálā Copilot 🪄
**Kálā Copilot** aims to fix this invisibility problem. It’s an AI-driven sidekick that helps creators bring their products online, without needing a marketing degree or advanced tech skills.

### 2.1 What does it actually do?
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

### 2.2 How does it work under the hood?
Multiple specialized AI agents collaborate in a pipeline, each handling a unique piece of the process:

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
Kálā Copilot is primarily built for:

- **Artisans & Skilled Creators** lacking digital or marketing support.  
- **Small/Micro Business Owners** selling through WhatsApp, Instagram, Meesho, Etsy... but who need help generating persuasive content.  
- **Digital-First Sellers** in underserved regions or minority-owned businesses that don’t have marketing teams.

**Example:**  
Rani, a weaver from Bihar, crafts a Banarasi silk saree over several weeks. Online marketing is alien to her—she doesn’t know how to price, describe, or tag her work. Kálā Copilot steps in to seamlessly generate an entire campaign (in her language), giving Rani the digital push she deserves.

---

## 4. Business Relevance
For **hackathon judges**, this section highlights the commercial viability:  
Kálā Copilot isn’t just a neat trick; it’s a gateway for **ecommerce growth** in emerging markets.

- **Ecommerce Platforms (Meesho, Flipkart, Amazon India)** can tap into new seller segments by providing instant, high-quality listings.  
- **Improved Listings & Data** benefit both marketplaces and end customers: better discoverability, more relevant search results.  
- **Culturally Localized Content** expands commerce in multiple languages and geographies.  
- **Scalable Impact**: each new user becomes a self-sufficient micro-brand, no marketing team required.

Essentially, it unlocks an untapped market of creative entrepreneurs—each with endless product potential.

---

## 5. Technical Overview
In this section, we outline the modular architecture that powers Kálā Copilot. Our system employs a chain-of-agents approach, ensuring each AI agent focuses on a specific task.

### 5.1 Modular Agents: The Brains Behind Kálā Copilot 🧠
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
       width="80%" style="max-width:600px;" />
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
| Twitter API                | Publishes marketing content                             |
| GitHub Copilot             | Provided some code suggestions, then vanished mysteriously 👀 |

---

### 5.5 Solution Quality Highlights
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

It all started with a spark of curiosity.  
[@ipshitag](https://github.com/ipshitag), [@sougaaat](https://github.com/sougaaat), and [@manish-kt](https://github.com/manish-kt) often dive into random rabbit holes involving data and social impact. A course about the history of Indian crafts led [@ipshitag](https://github.com/ipshitag) to discover a heartbreaking truth: even **National Award-winning** artisans struggle for visibility and fair markets.

Fueled by frustration (and a lot of caffeine), the trio realized:  
_"We have to fix this."_  

That’s how **Kálā Copilot** was born—a solution stitched with Python, powered by Azure, and brimming with love for traditional craftsmanship. Our team members hail from places like Jaipur, Kolkata, and Ranchi—cities where art is more than a hobby; it’s a lifeline, identity, and pride.

We asked ourselves:  
_"What if AI could help artisans become their own digital marketers?"_  

And here we are, unveiling **Kálā Copilot** as a small but determined step toward bridging the gap between local creators and the global marketplace.

> “Art is the most intense mode of individualism that the world has known.”  
> — Oscar Wilde  
</details>

---

<!-- END OF README -->
