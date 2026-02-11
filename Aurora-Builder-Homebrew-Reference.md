# Aurora Builder Homebrew – Complete Reference (No External Links)

## Overview

This document is a self-contained guide to creating, testing, and distributing homebrew content for **Aurora Builder** (a D&D 5e character builder). It consolidates what the official documentation, example repositories, and community projects show about:

- How Aurora's XML content format works.
- How local and hosted content is structured and loaded.
- How to organize a homebrew repository others can subscribe to.
- Practical workflows and patterns used in real homebrew packs.[cite:1][cite:5]

---

## 1. Core Concepts of Aurora Homebrew

Aurora's rules and content (both official and homebrew) are defined in **XML files**. Each XML file contains a collection of `<element>` nodes inside a root `<elements>` tag.[cite:5]

Key ideas:

- Every race, class, feat, spell, item, background, feature, and so on is represented as an `<element>`.
- Each element has attributes and child tags that define:
  - How it appears in the UI (name, description, source).
  - How it behaves mechanically (rules, stats, proficiencies, spell lists).
- Aurora merges content from:
  - Built-in sources.
  - Downloaded content packs (via **index files**).
  - Local custom folders inside your user profile.[cite:1]

Because of this, homebrew is just **additional XML elements** that follow the same structure and conventions as the official content.

---

## 2. Content File Structure (XML Details)

### 2.1 File-Level Structure

Each content file is a standard XML document:

- It begins with an XML declaration.
- The root element is `<elements>`.
- Inside `<elements>` are one or more `<element>` entries.

A minimal file shape:

```xml
<?xml version="1.0" encoding="utf-8"?>
<elements>
  <!-- One or more elements go here -->
</elements>
```

Aurora scans all such files in its content folders and integrates each `<element>` into its internal database.[cite:5]

### 2.2 Element Attributes

Every `<element>` node generally has at least these attributes:

- `name` – The in-game display name (e.g. "Battle Smith").
- `type` – The kind of content, examples:
  - `Race`
  - `Sub Race`
  - `Class`
  - `Archetype` (subclass)
  - `Background`
  - `Feat`
  - `Spell`
  - `Equipment`
  - `Feature`
  - and more, depending on what is being defined.
- `source` – The book, setting, or homebrew collection name it belongs to (e.g. "Homebrew – YourName").
- `id` – A unique identifier string that Aurora uses internally.

The `id` should be globally unique across all content. A common pattern looks like:

- `ID_INTERNAL_SOMETHING`
- `ID_HOMEBREW_YOURNAME_RACE_EXAMPLE`
- `ID_HOMEBREW_YOURNAME_CLASS_EXAMPLE`

Consistency and uniqueness of `id` values is critical for avoiding conflicts when mixing multiple content packs.[cite:5][cite:6]

### 2.3 Typical Child Tags

While details vary by element type, several child tags are used everywhere:

- `<description>`  
  Contains formatted text describing the element. This often uses HTML-like tags:
  - `<p>` – paragraphs.
  - `<strong>` – bold emphasis.
  - `<em>` – italics.
  - `<ul>`, `<li>` – lists.
- `<rules>`  
  Defines mechanical effects, often with nested tags like:
  - `<stat>` – changes to ability scores or other numeric stats.
  - `<grant>` – giving features, proficiencies, or other elements.
  - `<select>` – allowing choices (e.g. choose a weapon proficiency).
  - `<skillproficiency>` or similar tags for specific proficiencies.

Example snippet for a subrace that boosts Strength:

```xml
<element name="Example Dwarf" type="Sub Race" id="ID_HOMEBREW_EXAMPLE_DWARF" source="Homebrew – YourName">
  <supports>Dwarf</supports>
  <description>
    <p>Your flavorful description here.</p>
  </description>
  <rules>
    <stat name="strength" value="2" />
  </rules>
</element>
```

Key points illustrated:

- `<supports>Dwarf</supports>` states which base race this subrace attaches to.
- `<rules>` changes stats (here: +2 Strength).[cite:5]

Different element types (classes, feats, spells) use specialized child tags, but the pattern—**description plus rules**—is consistent across the official examples.[cite:6]

---

## 3. Local Content Loading and Folder Layout

Aurora looks for additional content in a **custom** folder under your documents directory. A typical Windows path:

```text
Documents\5e Character Builder\custom
```

Important subfolder:

- `custom\user` – This is where **local homebrew** goes. Aurora:
  - Reads everything in this folder.
  - Loads it **last**, so it can override other sources when there are conflicts.
  - Treats it as your personal sandbox and override layer.[cite:1][cite:5]

Typical workflow for local-only homebrew:

1. Create an XML file with a root `<elements>` tag.
2. Place it in `custom\user`.
3. Restart Aurora (or trigger a content reload).
4. Your new race/class/feat/etc. appears alongside official content.

Because `custom\user` is loaded last, you can:

- Redefine an existing element by giving it the **same `id`** as an official one but different rules.
- Test new content quickly without publishing it anywhere.

For general development and debugging, this folder is the best place to iterate on homebrew.[cite:1][cite:5]

---

## 4. Hosted Content and Index Files

To share homebrew with others (players or the public), Aurora supports **hosted content** that it downloads from the internet using **index files**.[cite:1][cite:6][cite:13]

### 4.1 What an Index File Is

An **index file** is a simple text file (with `.index` extension) that lists references to:

- Other `.index` files.
- Actual `.xml` content files.

Aurora starts from an index and recursively follows every reference it finds, downloading all needed XMLs.

Conceptual example of a simple index structure:

- `myhomebrew.index`
  - references `myhomebrew-core.xml`
  - references `myhomebrew-spells.xml`
  - references `myhomebrew-feats.xml`

When a user pastes the address of `myhomebrew.index` into Aurora's Additional Content screen:

1. Aurora downloads `myhomebrew.index`.
2. Reads the entries.
3. Downloads each listed XML file (and any nested indexes).
4. Stores them under the `custom` folder.
5. Loads them at startup like any other content.[cite:1][cite:6][cite:13]

### 4.2 Additional Content Workflow (From the User's Perspective)

Inside Aurora, there is an **Additional Content** section accessible from the start screen. The workflow is:

1. Open Aurora.
2. Navigate to the Additional Content / Content Repository section.
3. Add a new content source by providing an index file address (for example, the "raw" form of a file hosted on a version control platform).
4. Aurora downloads and caches the corresponding content.
5. After restart, the new source appears in your **Sources** list, and all races/classes/feats/items defined by that source are available for characters.[cite:1][cite:6][cite:8]

This is how the official extended content libraries and large community packs are distributed.

---

## 5. Official Example Library ("Elements") – What It Contains

Aurora's main public example library is often referred to as the **elements repository**. It contains:

- All core official content from the primary game books.
- Supplements.
- Unearthed Arcana material.
- Some third‑party content where allowed.[cite:1][cite:6]

### 5.1 Organization Style

The elements library uses a **hierarchical structure** with:

- Top-level index files for categories such as:
  - Core content.
  - Supplements.
  - Unearthed Arcana.
  - Third‑party sources.
- Sub-indexes for each book or grouped source.
- Collections of `.xml` files representing:
  - Races and subraces.
  - Classes and archetypes.
  - Backgrounds.
  - Feats.
  - Spells.
  - Equipment.
  - Features and rules components.[cite:6][cite:13]

For example, a core category might be structured conceptually as:

- `core.index`
  - references `players-handbook.index`
    - which references:
      - `races-phb.xml`
      - `classes-phb.xml`
      - `backgrounds-phb.xml`
      - `feats-phb.xml`
  - references `basic-rules.index`
  - and so on.

### 5.2 How to Use the Elements Library for Homebrew

To create homebrew:

1. Identify what you are making:
   - New race or subrace.
   - New subclass (archetype).
   - New feat, item, spell, or background.
2. In the elements library, find the relevant official example for that type.
3. Open the XML file.
4. Copy an `<element>` that is close to what you want.
5. Paste it into your own XML file (under `<elements>`).
6. Change:
   - `name` to your homebrew's name.
   - `id` to a unique new identifier.
   - `source` to your custom source name.
   - Description text.
   - Rules (stats, proficiencies, features) as appropriate.[cite:6][cite:13]

Because every official feature in the game is represented there, this library is effectively a **dictionary of patterns**:

- How to define casting progressions.
- How to implement new archetype features at specific levels.
- How to attach a subrace to its parent race.
- How to model spells (components, range, duration, school, scaling).
- How to model equipment (weight, value, rarity, properties).

Studying these real, working examples removes guesswork from the XML format.

---

## 6. Template for Homebrew Repositories

To help creators build their own shareable content packs, Aurora provides a **repository template** for homebrew.

### 6.1 Structure of the Template

The template contains:

- A top-level index file named in the pattern:
  - `user-yourname.index`
- A folder named similarly, for example:
  - `user-yourname/`
- A README explaining how to customize the template and how users should add your content into Aurora.[cite:6]

Within the content folder you will place your XML files, such as:

- `user-yourname/my-races.xml`
- `user-yourname/my-classes.xml`
- `user-yourname/my-items.xml`

The `user-yourname.index` file lists these XML files (and/or sub-indexes). Aurora reads this one index file, which in turn points to everything else.

### 6.2 Customizing the Template

The template uses placeholders that you must replace:

- `yourname` – Choose an identifier (often your handle).
- `yourgithubaccount` – Your account name on the hosting platform.
- `repositoryname` – The repository/project name.

You edit:

- The index filename and folder names to replace `yourname`.
- The paths in the index file to point to your actual XML files.
- The README text so that:
  - It shows your name.
  - It describes how to add your index address in Aurora.[cite:6]

### 6.3 How Users Subscribe to Your Repository

Once you host your repo:

1. Users open the Aurora Additional Content screen.
2. They add the address of your top-level index file (such as the "raw" view of `user-yourname.index`).
3. Aurora downloads your XML files and loads them as a new source.
4. Your homebrew appears in their Sources list and becomes available in character creation.

This pattern is used both for official extended libraries and larger community homebrew packs.[cite:6][cite:13]

---

## 7. Community Repository Patterns (What Others Do)

Several community homebrew repositories illustrate how to:

- Organize large, multi-source content.
- Merge official and custom material.
- Package single-creator content.[cite:9][cite:12][cite:14]

### 7.1 Large Multi-Source Pack Pattern

A typical large pack:

- Contains many folders, each representing a **book or line of content**, such as:
  - Third‑party campaign settings.
  - Additional monster books.
  - Homebrew subclasses from various authors.
- Has multiple index files:
  - One per large "module".
  - A combined index for "load everything".

Structure sketch:

- `bigpack.index` (combined all-in-one index)
- `bigpack-setting.index` (only the setting content)
- `bigpack-feats.index` (only feats)
- Folders with XML files grouped by theme or publisher.

Advantages:

- Users can choose between loading:
  - The entire pack.
  - Only specific parts (for example, just feats from a popular third‑party book).
- Easier maintenance as the creator can update one module at a time.[cite:14]

### 7.2 Merged Official + Homebrew Library Pattern

Some DMs maintain a library that:

- Mirrors the structure of the official elements library.
- Adds custom content alongside the official files.

Typical features:

- Index files that include both:
  - The canonical files from official content.
  - Additional homebrew XMLs.
- Carefully chosen IDs so that:
  - Custom elements do not conflict with official IDs.
  - Overrides (when desired) use the same IDs intentionally.

This pattern is helpful when:

- A DM wants a single "all-in-one" source set for their table.
- Players can subscribe once and get everything used in that campaign.[cite:9]

### 7.3 Single-Author / Small Pack Pattern

Smaller repos from individual creators often have:

- One main index.
- One folder containing a handful of XML files.
  - For example, a file of subclasses from one designer.
  - A file of magic items used in a personal campaign.

Structural characteristics:

- Simple and easy to navigate.
- Often grouped by content type (spells vs items) or by "booklet" (e.g. "Subclass Compendium").

These are good references when you want a **minimal** homebrew repository for just your group's content.[cite:3][cite:12]

---

## 8. Practical Step-by-Step Workflow

This section combines all information above into a concrete process for creating Aurora homebrew.

### Step 1 – Prepare Your Tools

1. Install a code-friendly text editor (e.g. VS Code).
2. Add XML-related extensions:
   - Syntax highlighting.
   - Auto-closing and validation.
3. Optionally configure snippets for common Aurora tags to speed up editing.[cite:5]

### Step 2 – Decide Local vs Hosted

- **Local-only / development:**
  - Use `Documents\5e Character Builder\custom\user`.
  - Fastest iteration: edit XML → restart Aurora → test.
- **Hosted / shareable:**
  - Use the official repository template.
  - Set up a public repository.
  - Plan to give players the address of your top-level index so they can subscribe.[cite:1][cite:6]

For early prototyping, start local; once stable, migrate files into a hosted repository.

### Step 3 – Choose a Reference Example

1. Identify the content type you're making:
   - Race or subrace.
   - Class or subclass.
   - Background.
   - Feat.
   - Spell.
   - Equipment or item.
2. Inspect the corresponding official XML in the elements library:
   - Races show how ability scores, languages, and traits are structured.
   - Classes and archetypes show how level-based features and spellcasting are implemented.
   - Spells show metadata (level, school, casting time, components, duration) and rules.
   - Equipment shows cost, weight, damage, properties, and categories.[cite:6][cite:13]
3. Pick one closely matching element as a **template**.

### Step 4 – Create Your XML File

1. Create a new `.xml` file with:

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <elements>
   </elements>
   ```

2. Paste your chosen template `<element>` inside `<elements>`.
3. Edit its attributes:
   - `name` – change to your homebrew's name.
   - `id` – change to a unique identifier following your own naming convention.
   - `source` – set to a meaningful source label (e.g. "Homebrew – YourName").
4. Edit its child tags:
   - Update `<description>` to your text, using paragraphs and formatting tags.
   - Modify or add `<rules>` entries:
     - Adjust stats via `<stat>` nodes.
     - Add or remove features via `<grant>` nodes.
     - Change skill or weapon proficiencies using the appropriate tags.
     - For classes, ensure features appear at correct levels.
     - For spells, set correct level, school, components, range, duration, and effects.

5. If your homebrew comprises multiple elements, define each as its own `<element>` block in the same file or split them across multiple files as you prefer.

### Step 5 – Test Locally

1. Place your XML file into:

   ```text
   Documents\5e Character Builder\custom\user
   ```

2. Restart Aurora so it reloads content.
3. In Aurora:
   - Check that your **source** name appears where appropriate.
   - Attempt to create a character using your race/class/feat/spell/etc.
   - Verify:
     - Bonuses are applied correctly.
     - Features show up at correct levels.
     - Spells are selectable where expected.
     - Items show correct stats.

4. Fix any issues by editing the XML and repeating the cycle.

This loop benefits from comparing your file side-by-side with known-good official examples.[cite:2][cite:4][cite:11]

### Step 6 – Build a Hosted Repository (Optional but Recommended)

When your homebrew is stable and you want to share it:

1. Start from the official repository template.
2. Replace placeholders (`yourname`, `yourgithubaccount`, `repositoryname`) in:
   - Folder names.
   - Index file names.
   - README text.
3. Move your tested XML files into the template's content folder (e.g. `user-yourname/`).
4. Update the top-level index (`user-yourname.index`) to reference your XML files and any sub-indexes.
5. Commit and publish the repository.[cite:6]

### Step 7 – Give Players the Index Address

1. Determine the public address of your `user-yourname.index` file (for example, the direct "raw" view on a code hosting site).
2. Share this address with your players.
3. In their Aurora installations, they:
   - Open Additional Content.
   - Add a new source with your index address.
   - Download or update.
4. After a restart, your homebrew appears as a source and is ready for use.[cite:1][cite:6][cite:8][cite:13]

### Step 8 – Grow and Maintain the Pack

As your homebrew expands:

- Group content logically:
  - By type (spells vs feats).
  - By sub-setting or book.
- Introduce sub-indexes for large modules, similar to the official elements library and large community packs.
- Maintain a change log or versioning scheme so players know when to refresh their content.
- Periodically validate that:
  - IDs remain unique across all your files.
  - No deprecated tags or structures are left from old experiments.

Studying established community packs (small, medium, and large) is a good way to refine your layout over time.[cite:3][cite:9][cite:12][cite:14]

---

## 9. Conceptual Summary

- **Everything is XML**: Aurora's entire ruleset, including homebrew, is defined by XML `<element>` nodes inside `<elements>`.[cite:5][cite:6]
- **Local homebrew**:
  - Lives in `Documents\5e Character Builder\custom\user`.
  - Is loaded last and can override other content.
  - Is ideal for rapid iteration.
- **Hosted homebrew**:
  - Uses index files that point to XML content.
  - Is added through Aurora's Additional Content screen.
  - Enables sharing and auto-updating for players.
- **Official examples** provide the language of the system:
  - Show exactly how to implement every kind of element.
  - Should be copied and adapted rather than reinvented from scratch.
- **Repository templates and community packs** show:
  - How to structure multi-source and single-author projects.
  - How to scale from a small set of personal items to a full-blown "book" worth of content.

With this information, you can design, implement, test, and distribute Aurora-compatible homebrew in a way that matches how official and community content is already structured.

---
