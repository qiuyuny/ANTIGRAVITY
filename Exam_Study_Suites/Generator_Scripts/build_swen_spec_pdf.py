# -*- coding: utf-8 -*-
"""
SWEN20003 Object Oriented Software Development
Open-Book Exam Cheat Sheet & Reference Manual (Spec Edition)
Part I: Visual Topic Tree Index | Part II: Lookup Tables, UML Rules, SOLID & Java Templates
"""

import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    HRFlowable, PageBreak, Table, TableStyle
)
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont('SegoeUI', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeUIBold', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFont(TTFont('ConsolasBold', 'C:/Windows/Fonts/consolab.ttf'))

title_style = ParagraphStyle(
    'TitleStyle', fontName='SegoeUIBold', fontSize=14.5, leading=19,
    textColor=colors.black, spaceAfter=3
)
sub_style = ParagraphStyle(
    'SubStyle', fontName='Consolas', fontSize=8.8, leading=11.5,
    textColor=colors.HexColor('#333333'), spaceAfter=7
)
h2_style = ParagraphStyle(
    'H2Style', fontName='SegoeUIBold', fontSize=10.8, leading=14,
    textColor=colors.white, backColor=colors.black,
    borderPadding=(4, 6, 4, 6), spaceBefore=10, spaceAfter=5
)
h3_style = ParagraphStyle(
    'H3Style', fontName='SegoeUIBold', fontSize=9.6, leading=12.8,
    textColor=colors.black, backColor=colors.HexColor('#E8E8E8'),
    borderPadding=(2, 4, 2, 4), spaceBefore=7, spaceAfter=4
)
code_style = ParagraphStyle(
    'CodeStyle', fontName='Consolas', fontSize=7.7, leading=10.0,
    textColor=colors.black, backColor=colors.HexColor('#F6F6F6'),
    borderPadding=4.5, leftIndent=4, rightIndent=4, spaceBefore=2, spaceAfter=4
)
tree_style = ParagraphStyle(
    'TreeStyle', fontName='Consolas', fontSize=7.9, leading=10.2,
    textColor=colors.black
)
th_style = ParagraphStyle(
    'THStyle', fontName='SegoeUIBold', fontSize=8.3, leading=10.8,
    textColor=colors.black
)
td_text_style = ParagraphStyle(
    'TDTextStyle', fontName='SegoeUI', fontSize=8.1, leading=10.8,
    textColor=colors.black
)

def clean_and_esc(s):
    replacements = [
        ('⇔', ' iff '), ('∀', 'for all '), ('∃', 'there exists '),
        ('∈', ' in '), ('⊆', ' subset of '),
        ('≤', '<='), ('≥', '>='), ('→', '->'), ('≠', '!='),
        ('«', '<<'), ('»', '>>')
    ]
    s = str(s)
    for k, v in replacements:
        s = s.replace(k, v)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("&lt;br/&gt;", "<br/>").replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    s = s.replace("\n", "<br/>")
    return s

def make_table(headers, rows, col_widths=None):
    data = [[Paragraph(clean_and_esc(h), th_style) for h in headers]]
    for r in rows:
        data.append([Paragraph(clean_and_esc(c), td_text_style) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DFDFDF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 4.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4.5),
    ]))
    return t

TREE_TEXT = """[!!!] = Core / Must-know    [!! ] = Important / Frequent    [!  ] = Basic / Edge case

[0.0] SWEN20003 OBJECT-ORIENTED SOFTWARE DEVELOPMENT (JAVA)
│
├── [1.0] Java Memory Model, Strings, Arrays & Immutability
│   ├── [1.1] Primitives, References & String Pool
│   │   ├── [1.1.1] Stack primitives vs Heap reference variables         [!! ]
│   │   ├── [1.1.2] Reference equality (==) vs value equality (.equals)  [!!!]
│   │   ├── [1.1.3] String literal pool vs new String() & StringBuilder  [!! ]
│   │   └── [1.1.4] Wrapper classes, Autoboxing/Unboxing & Integer cache [!! ]
│   │
│   ├── [1.2] Encapsulation, Privacy Leaks & Immutability
│   │   ├── [1.2.1] Access modifiers (private, package, protected, pub)  [!!!]
│   │   ├── [1.2.2] Information hiding & constructor/getter privacy leak [!!!]
│   │   ├── [1.2.3] Defensive copying (deep copy in constructor/getter)  [!!!]
│   │   └── [1.2.4] Complete Immutable Class 5-step recipe               [!!!]
│   │
│   └── [1.3] Static vs Instance & Parameter Passing
│       ├── [1.3.1] Pass-by-value semantics for primitives & references  [!!!]
│       └── [1.3.2] Static fields/methods, final constants & utility cls [!! ]
│
├── [2.0] Inheritance, Polymorphism, Binding & Abstract Types
│   ├── [2.1] Inheritance Mechanics & Constructor Chaining
│   │   ├── [2.1.1] extends keyword, single inheritance & super() rules  [!!!]
│   │   ├── [2.1.2] Upcasting (implicit safe) vs Downcasting + instanceof[!!!]
│   │   └── [2.1.3] Object cosmic superclass (toString, equals, hashCode)[!!!]
│   │
│   ├── [2.2] Polymorphism, Overriding vs Overloading & Dispatch
│   │   ├── [2.2.1] Static (declared) type vs Dynamic (actual) type      [!!!]
│   │   ├── [2.2.2] Method Overriding (@Override) & dynamic binding      [!!!]
│   │   ├── [2.2.3] Method Overloading & compile-time static binding     [!!!]
│   │   └── [2.2.4] Field hiding & static method hiding (compile-time)   [!! ]
│   │
│   └── [2.3] Abstract Classes vs Interfaces
│       ├── [2.3.1] Abstract classes & abstract method contracts         [!!!]
│       ├── [2.3.2] Interfaces (implements, multiple inheritance of type)[!!!]
│       └── [2.3.3] Abstract Class ("IS-A") vs Interface ("CAN-DO")      [!!!]
│
├── [3.0] UML Class Diagrams & OO Design Principles
│   ├── [3.1] UML Class Box & Visibility Notation
│   │   ├── [3.1.1] 3-compartment box: Name, Attributes, Operations      [!!!]
│   │   └── [3.1.2] Visibility symbols (-, +, #, ~) & static underline   [!!!]
│   │
│   ├── [3.2] Six Core UML Class Relationships & Multiplicities
│   │   ├── [3.2.1] Association & Navigability arrow + Multiplicity      [!!!]
│   │   ├── [3.2.2] Aggregation (Hollow Diamond) weak whole-part         [!!!]
│   │   ├── [3.2.3] Composition (Filled Solid Diamond) strong lifecycle  [!!!]
│   │   ├── [3.2.4] Inheritance / Generalization (Solid line, hollow tri)[!!!]
│   │   ├── [3.2.5] Realization / Interface (Dashed line, hollow tri)    [!!!]
│   │   └── [3.2.6] Dependency (Dashed line, open arrow)                 [!! ]
│   │
│   └── [3.3] Coupling, Cohesion & Delegation
│       ├── [3.3.1] Low Coupling & High Cohesion design evaluation       [!!!]
│       └── [3.3.2] Favor Composition/Delegation over Inheritance        [!!!]
│
├── [4.0] SOLID Principles & Gang of Four (GoF) Design Patterns
│   ├── [4.1] SOLID Design Principles
│   │   ├── [4.1.1] Single Responsibility Principle (SRP)                [!!!]
│   │   ├── [4.1.2] Open/Closed Principle (OCP)                          [!!!]
│   │   ├── [4.1.3] Liskov Substitution Principle (LSP)                  [!! ]
│   │   ├── [4.1.4] Interface Segregation Principle (ISP)                [!! ]
│   │   └── [4.1.5] Dependency Inversion Principle (DIP)                 [!! ]
│   │
│   └── [4.2] Gang of Four (GoF) Design Patterns
│       ├── [4.2.1] Singleton Pattern (Creational: 1 lazy instance)      [!!!]
│       ├── [4.2.2] Strategy Pattern (Behavioural: swappable algorithms) [!!!]
│       ├── [4.2.3] State Pattern (Behavioural: state-driven transitions)[!!!]
│       ├── [4.2.4] Observer Pattern (Behavioural: 1-to-many pub/sub)    [!!!]
│       ├── [4.2.5] Template Method Pattern (Behavioural: skeleton algo) [!!!]
│       └── [4.2.6] Factory / Adapter / Decorator pattern recognition    [!  ]
│
├── [5.0] Generics, Collections, Sorting & Streams
│   ├── [5.1] Parametric Polymorphism (Generics)
│   │   ├── [5.1.1] Generic classes/methods <T, K, V> & type safety      [!!!]
│   │   ├── [5.1.2] Bounded type parameters <T extends UpperBound>       [!!!]
│   │   └── [5.1.3] Wildcards (<?>, <? extends T>, <? super T>) & erasure[!! ]
│   │
│   ├── [5.2] Java Collections Framework (List, Set, Map, Queue)
│   │   ├── [5.2.1] ArrayList vs LinkedList & Iterator safe removal      [!!!]
│   │   ├── [5.2.2] HashMap<K,V> & nested Map<K, ArrayList<V>> patterns  [!!!]
│   │   └── [5.2.3] HashSet/TreeSet & equals()/hashCode() contract       [!! ]
│   │
│   └── [5.3] Object Comparison & Functional Streams
│       ├── [5.3.1] Comparable<T> (compareTo) vs Comparator<T> (compare) [!!!]
│       └── [5.3.2] Lambda expressions & Stream pipeline (filter/map/sort)[!! ]
│
└── [6.0] Exceptions, File I/O, Event-Driven GUI & Testing
    ├── [6.1] Exception Handling Architecture
    │   ├── [6.1.1] Throwable hierarchy: Checked vs Unchecked (Runtime)  [!!!]
    │   ├── [6.1.2] try-catch-finally execution order & multi-catch      [!!!]
    │   └── [6.1.3] try-with-resources (AutoCloseable) & custom Exception[!!!]
    │
    ├── [6.2] File I/O & Text Processing
    │   ├── [6.2.1] BufferedReader / FileReader / Scanner / PrintWriter  [!! ]
    │   └── [6.2.2] CSV parsing (.split(",")) & String formatting        [!! ]
    │
    └── [6.3] Event-Driven Programming & Automated Testing
        ├── [6.3.1] Event-driven loop, Listeners/Handlers & MVC decouple [!! ]
        └── [6.3.2] Automated Unit Testing (JUnit @Test, assertions)     [!!!]"""

def build_pdf(target_path):
    doc = SimpleDocTemplate(
        target_path, pagesize=A4,
        leftMargin=26, rightMargin=26, topMargin=24, bottomMargin=24
    )
    W = A4[0] - 52
    s = []

    s.append(Paragraph("SWEN20003 OPEN-BOOK EXAM CHEAT SHEET & REFERENCE MANUAL", title_style))
    s.append(Paragraph("Part I: Visual Topic Tree Index  |  Part II: OOP Lookup Tables, UML Rules, Design Patterns & Java Templates", sub_style))
    s.append(HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceAfter=6))

    # Scope Table
    s.append(make_table(
        ["IN-SCOPE (Core Exam Syllabus)", "OUT-OF-SCOPE (Never Tested)"],
        [[
            "• Java Memory, String Pool, Wrappers, Immutability & Defensive Copy<br/>"
            "• Inheritance, Polymorphism, Overriding vs Overloading Dispatch<br/>"
            "• Abstract Classes vs Interfaces, Upcasting/Downcasting<br/>"
            "• Reading & Drawing UML Class Diagrams (Multiplicity, Diamonds)<br/>"
            "• SOLID Principles (SRP, OCP, LSP, ISP, DIP) & Code Critique<br/>"
            "• GoF Patterns: Strategy, Singleton, Observer, Template Method, State<br/>"
            "• Generics (<T extends X>), ArrayList, HashMap, Comparable/Comparator<br/>"
            "• Checked vs Unchecked Exceptions, Streams, Automated Testing",
            "• Bagel / JavaFX Game Engine API Method Signatures<br/>"
            "• Gradle Build Scripts (build.gradle.kts) & Module Info Syntax<br/>"
            "• Complex Concurrency / Thread Locks (beyond Singleton synchronized)<br/>"
            "• Bytecode / JVM Garbage Collector Internal Algorithms<br/>"
            "• Network Socket Programming or SQL Database JDBC Drivers<br/>"
            "• Memorizing Java Standard Library Appendix Docs (provided in exam)"
        ]],
        col_widths=[W*0.53, W*0.47]
    ))
    s.append(Spacer(1, 5))

    s.append(Paragraph("PART I · VISUAL TOPIC TREE INDEX", h2_style))
    s.append(Preformatted(TREE_TEXT, tree_style))

    s.append(PageBreak())
    s.append(Paragraph("PART II · OPEN-BOOK REFERENCE TABLES, UML RULES & JAVA TEMPLATES", h2_style))

    # ================= MODULE 1 =================
    s.append(Paragraph("[1.0] Java Memory Model, Encapsulation, Privacy Leaks & Immutability", h3_style))
    s.append(make_table(
        ["Index & Topic", "Java Rule / Mechanism", "Critical Exam Trap / Fix"],
        [
            ["[1.1.2] == vs .equals()", "• == compares primitive values OR memory addresses (references)\n• .equals() compares logical object content (must override Object.equals)", "NEVER use == to compare Strings or Wrapper objects! Always use s1.equals(s2)"],
            ["[1.1.3] String Pool", "• String s1 = \"hi\"; uses shared String Constant Pool on heap\n• String s2 = new String(\"hi\"); forces a new distinct heap object", "s1 == s2 is FALSE, but s1.equals(s2) is TRUE.\nUse StringBuilder in loops to avoid O(n^2) String allocations"],
            ["[1.1.4] Wrapper Cache", "• Autoboxing: Integer a = 100; (calls Integer.valueOf(100))\n• Java caches Integer instances in range [-128, 127]", "Integer a=100, b=100 -> a==b is TRUE (cached).\nInteger x=200, y=200 -> x==y is FALSE (new heap objects)!"],
            ["[1.2.1] Access Modifiers", "• private: same class only   • (default/package): same package\n• protected: same package + subclasses anywhere   • public: everywhere", "Encapsulation rule: ALL instance fields must be private (or private final)"],
            ["[1.2.2] Privacy Leak\n& Defensive Copy", "• Leak 1 (Constructor): this.list = list; (caller keeps reference to mutable list)\n• Leak 2 (Getter): return this.list; (caller mutates internal list via getter)", "• Fix 1 (Constructor): this.list = new ArrayList<>(list);\n• Fix 2 (Getter): return new ArrayList<>(this.list);  (or Collections.unmodifiableList)"],
            ["[1.2.4] Immutable Class\n5-Step Checklist", "1. Declare class as public final class ... (prevents subclassing)\n2. Declare all fields as private final\n3. Do NOT provide any setter (mutator) methods", "4. In Constructor: perform deep defensive copy of all mutable input parameters\n5. In Getters: return deep defensive copies of all mutable fields (String/primitives are already immutable, so direct return is safe)"]
        ],
        col_widths=[W*0.23, W*0.42, W*0.35]
    ))
    s.append(Spacer(1, 3))
    s.append(Preformatted(
"""/* [1.2.4] Complete Exam-Ready Immutable Class Template with Defensive Copying */
public final class ImmutablePerson {
    private final String name;                 // String is already immutable -> safe
    private final List<String> hobbies;        // List is mutable -> MUST defensive copy!

    public ImmutablePerson(String name, List<String> hobbies) {
        this.name = name;
        this.hobbies = new ArrayList<>(hobbies);   // Line A Fix: Defensive copy on input!
    }
    public String getName() { return this.name; }
    public List<String> getHobbies() {
        return new ArrayList<>(this.hobbies);      // Line B Fix: Defensive copy on output!
    }
}""", code_style))

    # ================= MODULE 2 =================
    s.append(Paragraph("[2.0] Inheritance, Polymorphism, Overriding vs Overloading & Abstract Types", h3_style))
    s.append(make_table(
        ["Index & Feature", "Compile-Time (Static) Rule", "Run-Time (Dynamic) Execution Rule"],
        [
            ["[2.2.1] Static vs Dynamic\nType: Base b = new Sub();", "• Static (Declared) Type = Base\n• Compiler checks ONLY Base class to verify if method/field exists", "• Dynamic (Actual Heap) Type = Sub\n• JVM dispatches overridden instance methods based on Sub at runtime"],
            ["[2.2.2] Method Overriding\n(@Override)", "• Exact same method name AND exact same parameter types in subclass\n• Return type must be same (or covariant subtype); visibility cannot be narrower", "• DYNAMIC BINDING (Late Binding):\n  JVM runs the Subclass implementation based on actual heap object type"],
            ["[2.2.3] Method Overloading\n(Classic Exam Trap!)", "• Same method name, DIFFERENT parameter list (type, count, or order)\n• Can occur in same class OR between superclass and subclass", "• STATIC BINDING (Early Binding):\n  Compiler locks the exact method signature at compile time using ONLY the Static Declared Type of the caller variable and argument static types!"],
            ["[2.2.4] Static Methods &\nInstance Fields", "• Cannot override static methods or instance fields (only hides them)", "• STATIC BINDING: Resolved strictly at compile time using Static Declared Type"],
            ["[2.1.1] Constructor Chain", "• First line of subclass constructor MUST be super(...) or this(...)\n• If omitted, compiler automatically inserts implicit super() (no-arg)", "• If superclass has NO no-arg constructor, subclass MUST explicitly call super(args) on Line 1 or compilation fails!"],
            ["[2.1.2] Casting &\ninstanceof", "• Upcasting: Base b = new Sub(); (Always safe, implicit)\n• Downcasting: Sub s = (Sub) b; (Requires explicit cast)", "• If actual object is NOT a Sub, (Sub) b throws ClassCastException at runtime!\n• Always guard with: if (b instanceof Sub) { Sub s = (Sub) b; }"]
        ],
        col_widths=[W*0.24, W*0.38, W*0.38]
    ))
    s.append(Spacer(1, 3))
    s.append(make_table(
        ["[2.3.3] Dimension", "Abstract Class (abstract class A)", "Interface (interface I)"],
        [
            ["Core Relationship", "\"IS-A\" identity & shared code hierarchy (e.g., Staff -> Doctor, Receptionist)", "\"CAN-DO\" capability contract across unrelated classes (e.g., Comparable, Attackable)"],
            ["Multiple Inheritance", "Single inheritance ONLY: a class can extend at most ONE class", "Multiple implementation: a class can implement MANY interfaces (implements A, B, C)"],
            ["State & Fields", "Can hold non-final, private/protected instance variables (mutable state)", "NO instance fields! All fields are implicitly public static final constants"],
            ["Constructors & Methods", "Has constructors (called via super()); mixes concrete + abstract methods", "NO constructors; abstract methods (plus Java 8+ default/static utility methods)"]
        ],
        col_widths=[W*0.22, W*0.39, W*0.39]
    ))

    # ================= MODULE 3 =================
    s.append(Paragraph("[3.0] UML Class Diagrams, Relationships & OO Design Quality", h3_style))
    s.append(make_table(
        ["[3.2] UML Relationship", "Visual Arrow / Symbol Style", "Meaning, Lifecycle & Java Code Mapping"],
        [
            ["[3.2.1] Association", "Solid line with open arrow ( A ──────> B )", "• \"HAS-A\" / knows about: Class A holds a reference field to Class B (private B b;)\n• Multiplicity placed at target end: 1 (exact), 0..1 (optional), * or 0..* (many), 1..* (at least 1)"],
            ["[3.2.2] Aggregation\n(Weak Whole-Part)", "Solid line with HOLLOW WHITE diamond at Whole\n( Whole ◇────── Part )", "• \"HAS-A\" collection where Part CAN exist independently if Whole is destroyed\n• Exam Example: Department ◇────── Professor (if Department closes, Professor still lives)\n• Java Code: Whole receives Part via constructor/setter; holds List<Part>"],
            ["[3.2.3] Composition\n(Strong Whole-Part)", "Solid line with FILLED BLACK diamond at Whole\n( Whole ◆────── Part )", "• Exclusive ownership & LIFECYCLE DEPENDENCY: if Whole is destroyed, Parts cease to exist!\n• Exam Example: University ◆────── Department (or Car ◆────── Engine)\n• Java Code: Whole instantiates Part internally (this.part = new Part()) and never leaks it"],
            ["[3.2.4] Inheritance\n(Generalization)", "Solid line with HOLLOW TRIANGLE pointing to Super\n( Sub ──────▷ Super )", "• \"IS-A\" relationship between classes (class Sub extends Super)\n• Arrow ALWAYS points UP to the parent/superclass!"],
            ["[3.2.5] Realization\n(Implementation)", "DASHED line with HOLLOW TRIANGLE pointing to Interface\n( Class - - - -▷ «interface» )", "• \"CAN-DO\" implementation (class ConcreteStrategy implements Strategy)\n• Interface box is marked with guillemets «interface» above the name"],
            ["[3.2.6] Dependency", "DASHED line with open arrow ( A - - - -> B )", "• \"USES-A\" temporary relationship: A takes B as a method parameter, local var, or static call"]
        ],
        col_widths=[W*0.21, W*0.31, W*0.48]
    ))
    s.append(Spacer(1, 3))
    s.append(make_table(
        ["[3.1 / 3.3] Concept", "Notation / Definition", "Exam Justification & Application"],
        [
            ["[3.1.2] UML Visibility", "• - private    • + public    • # protected    • ~ package\n• Underlined = static   • Italics / {abstract} = abstract", "Attribute format:  - name : Type = defaultValue\nMethod format:     + methodName(param : Type) : ReturnType"],
            ["[3.3.1] Coupling vs\nCohesion (2017 Q1d)", "• Coupling: Degree of interdependence between different classes\n• Cohesion: Degree to which elements inside ONE class belong together", "• Goal: LOW Coupling + HIGH Cohesion\n• Low coupling makes classes easy to modify/reuse independently; high cohesion obeys SRP"],
            ["[3.3.2] Composition /\nDelegation > Inheritance", "• Delegation: Object hands over a task to a helper/strategy object field\n• Inheritance is fixed at compile time; Composition swaps behaviour at runtime", "• Avoids class explosion (e.g., MagicFlyingHero, MeleeFlyingHero)\n• Changes to superclass implementation do not break subclasses (fragile base class)"]
        ],
        col_widths=[W*0.21, W*0.39, W*0.40]
    ))

    s.append(PageBreak())

    # ================= MODULE 4 =================
    s.append(Paragraph("[4.0] SOLID Principles & Gang of Four (GoF) Design Patterns", h3_style))
    s.append(make_table(
        ["[4.1] SOLID Principle", "Core Definition", "Code Smell (Violation) -> Refactoring Solution"],
        [
            ["[4.1.1] S — Single\nResponsibility (SRP)", "A class should have one, and only one, reason to change (one cohesive responsibility).", "• Smell: OrderProcessor calculates discounts, executes SQL, AND sends emails.\n• Fix: Split into DiscountCalculator, OrderRepository, and EmailService."],
            ["[4.1.2] O — Open/Closed\nPrinciple (OCP)", "Software entities should be OPEN for extension, but CLOSED for modification.", "• Smell: if (type.equals(\"VIP\")) ... else if (type.equals(\"STUDENT\")) inside processor.\n• Fix: Introduce DiscountStrategy interface; add new classes without editing OrderProcessor."],
            ["[4.1.3] L — Liskov\nSubstitution (LSP)", "Subtypes must be substitutable for their base types without altering correctness.", "• Smell: Square extends Rectangle (setting width mutates height, breaking area tests) or subclass throws UnsupportedOperationException.\n• Fix: Extract common Shape interface instead of forcing invalid inheritance."],
            ["[4.1.4] I — Interface\nSegregation (ISP)", "Clients should not be forced to depend on fat interfaces with methods they do not use.", "• Smell: Fat Worker interface with work() and eat() forces Robot to implement dummy eat().\n• Fix: Split into smaller role interfaces Workable and Feedable."],
            ["[4.1.5] D — Dependency\nInversion (DIP)", "High-level modules should not depend on low-level concrete classes; both should depend on abstractions.", "• Smell: OrderProcessor directly calls new MySQLDatabase() or static EmailSender.\n• Fix: Depend on DatabaseInterface / NotificationService injected via constructor."]
        ],
        col_widths=[W*0.21, W*0.33, W*0.46]
    ))
    s.append(Spacer(1, 4))
    s.append(make_table(
        ["[4.2] GoF Pattern", "Family & Intent", "Participants & Structure", "When to Select in Exam / Key Benefit"],
        [
            ["[4.2.1] Singleton", "Creational:\nEnsure exactly ONE instance + global access point", "• Singleton class with:\n  1. private static Singleton instance;\n  2. private Singleton() {}\n  3. public static getInstance()", "• Logger, Database Connection Pool, Config Manager\n• Better than public static field: lazy initialization, prevents overwriting (instance = null), encapsulates creation logic"],
            ["[4.2.2] Strategy", "Behavioural:\nEncapsulate family of interchangeable algorithms (1-to-1)", "• Context (e.g., Course, Character)\n• Strategy Interface (e.g., DisplayStrategy)\n• ConcreteStrategies (SortByName, SortByGPA)", "• Switching attack/sorting/payment algorithms dynamically at runtime via setStrategy()\n• Satisfies OCP & replaces conditional if/else blocks"],
            ["[4.2.3] State", "Behavioural:\nObject alters behaviour when internal state changes", "• Context (e.g., Mokepon)\n• State Interface (ConditionState)\n• ConcreteStates (Asleep, Poisoned, Normal)", "• Entity has distinct states (Asleep/Poisoned/Confused) that change turn behaviour AND transition dynamically during battle"],
            ["[4.2.4] Observer", "Behavioural:\n1-to-Many publish-subscribe automatic notification", "• Subject (holds List<Observer>, add/remove/notify)\n• Observer Interface (update / onChanged)\n• ConcreteObservers (Timetable, Billing, LMS)", "• WeatherStation / EnrolmentSystem updates multiple displays/services without knowing their concrete classes (loose coupling, OCP)"],
            ["[4.2.5] Template\nMethod", "Behavioural:\nDefine algorithm skeleton in base class; defer steps to subclasses", "• AbstractClass (has final templateMethod() + abstract step methods)\n• ConcreteSubclasses (ExamReport, RPGGame)", "• Two classes share identical step sequence (open -> header -> body -> close) or game loop (input -> update -> render), differing only in specific steps"]
        ],
        col_widths=[W*0.16, W*0.22, W*0.30, W*0.32]
    ))
    s.append(Spacer(1, 3))
    s.append(Preformatted(
"""/* [4.2.1] Singleton Template */               /* [4.2.2] Strategy Pattern Template */             /* [4.2.4] Observer Subject Template */
public class Logger {                          public interface AttackStrategy {                   public class Subject {
    private static Logger instance = null;         int attack();                                       private List<Observer> obs = new ArrayList<>();
    private Logger() {} // Private!            }                                                       public void addObserver(Observer o) { obs.add(o); }
    public static Logger getInstance() {       public class Hero {                                     public void notifyObservers(String data) {
        if (instance == null) {                    private AttackStrategy strategy;                        for (Observer o : obs) {
            instance = new Logger();               public void setStrategy(AttackStrategy s) {                 o.update(data);
        }                                              this.strategy = s;                                  }
        return instance;                           }                                                   }
    }                                              public int performAttack() {                    }
}                                                      return strategy.attack(); // Delegate!      public interface Observer { void update(String d); }
                                                   }
                                               }""", code_style))

    # ================= MODULE 5 =================
    s.append(Paragraph("[5.0] Generics, Collections, Comparable vs Comparator & Streams", h3_style))
    s.append(make_table(
        ["Index & Topic", "Syntax / Contract", "Exam Coding Pattern & Pitfalls"],
        [
            ["[5.1.1] Generic Class", "public class Pair<T, U> {\n    private T first; private U second;\n}", "Instantiate with diamond operator: Pair<String, Integer> p = new Pair<>(\"A\", 1);\nType arguments MUST be Reference types (use Integer/Double, NEVER int/double)"],
            ["[5.1.2] Bounded Generics\n(2017 Exam Q6)", "public class CategorisedMap<K, V,\n    C extends Categoriser<V, K>>", "Always use keyword 'extends' for upper bounds in generic headers — even when Categoriser is an interface! Inside class, can safely call categoriser.categorise(val)"],
            ["[5.2.1] Iterator Removal", "Iterator<Student> it = list.iterator();\nwhile (it.hasNext()) {\n    if (it.next().getId().equals(id)) it.remove();\n}", "NEVER call list.remove(x) inside a for-each loop (for (Student s : list)) -> throws ConcurrentModificationException! Use Iterator.remove() or index loop"],
            ["[5.2.2] Nested HashMap\n(2016 Q3 / 2017 Q6)", "HashMap<K, ArrayList<V>> map = new HashMap<>();\nif (!map.containsKey(k)) map.put(k, new ArrayList<>());\nmap.get(k).add(val);", "When mapping one key to multiple values, check !map.containsKey(k) first and initialize the inner ArrayList<V> before calling .get(k).add(val) to avoid NullPointerException!"],
            ["[5.3.1] Comparable<T>\nvs Comparator<T>", "• Comparable<T> (Natural Order inside class):\n  public int compareTo(Card other)\n• Comparator<T> (External Strategy class/lambda):\n  public int compare(Card c1, Card c2)", "• Return sign rule:\n  • Ascending order:  return this.val - other.val; (or Double.compare(a, b))\n  • Descending order (2017 Q4a): return other.getPoints() - this.getPoints();\n• Sort call: Collections.sort(list);  OR  list.sort(comparator);"],
            ["[5.3.2] Java Streams\n(2017 Exam Q1f)", "list.stream()\n  .filter(m -> m.isActive())\n  .sorted((a, b) -> a.getScore() - b.getScore())\n  .collect(Collectors.toList());", "• .stream(): creates stream from collection without mutating original list\n• .filter(Predicate): keeps only elements where lambda returns true\n• .map(Function): transforms elements   • .sorted(Comparator): orders stream\n• .collect(Collectors.toList()): terminal op packaging results into a new List"]
        ],
        col_widths=[W*0.23, W*0.38, W*0.39]
    ))

    # ================= MODULE 6 =================
    s.append(Paragraph("[6.0] Exceptions, File I/O & Automated Software Testing", h3_style))
    s.append(make_table(
        ["Index & Topic", "Rules & Mechanics", "Exam Answers & Best Practices"],
        [
            ["[6.1.1] Checked vs\nUnchecked Exceptions", "• Checked (extends Exception, not RuntimeException): IOException, FileNotFoundException, SQLException. Compiler forces try-catch or 'throws' declaration.\n• Unchecked (extends RuntimeException): NullPointerException, IndexOutOfBoundsException, IllegalArgumentException, ClassCastException.", "Use Checked exceptions for recoverable external environment failures (missing file); use Unchecked exceptions for programming/logic bugs (null args, bad index)."],
            ["[6.1.2] Catch Ordering\n& Finally Block", "• Catch blocks MUST be ordered from MOST SPECIFIC (subclass) to MOST GENERAL (superclass), e.g., catch (FileNotFoundException) BEFORE catch (IOException).\n• finally block ALWAYS executes whether exception is thrown or not.", "Putting catch (Exception e) first causes a compile-time 'Unreachable catch block' error!\nUse try (BufferedReader br = new BufferedReader(...)) {} for automatic resource closing."],
            ["[6.3.2] Automated Testing\n(2017 Q1e & Q3b)", "• Automated Testing: Writing code/scripts (e.g. JUnit @Test) that automatically execute target methods with test inputs and assert expected outputs.", "• Two reasons preferred over manual testing:\n  1. Fast, repeatable regression testing on every code change without human effort.\n  2. Eliminates human error/fatigue and checks edge/boundary cases systematically.\n• Exam Test Case Format: (1) Component/Behaviour tested, (2) Concrete Input, (3) Expected Output/State."]
        ],
        col_widths=[W*0.22, W*0.42, W*0.36]
    ))

    doc.build(s)

out1 = r"C:\Users\kakur\Desktop\SWEN20003_Full_Exam_Spec.pdf"
out2 = r"C:\Users\kakur\Desktop\University\Semester_Current\SWEN20003_OOSD\SWEN20003_Full_Exam_Spec.pdf"

build_pdf(out1)
shutil.copyfile(out1, out2)
print("SWEN20003 Full Exam Spec PDF generated successfully!")

