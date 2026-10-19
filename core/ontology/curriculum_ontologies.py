"""
core/ontology/curriculum_ontologies.py
Standard Curriculum Ontologies for core technical disciplines:
- Python Core & OOP
- Java Standard Edition & OOP
- JavaScript / TypeScript Frontend
- Agile & Scrum Methodology
- SQL & Relational Databases
"""

from typing import Optional, Dict
from core.ontology.models import OntologyConcept, CurriculumOntologyGraph


def build_python_ontology() -> CurriculumOntologyGraph:
    graph = CurriculumOntologyGraph(tech_stack="python", domain_name="Python Core & Software Development")

    concepts = [
        OntologyConcept(
            concept_id="python_variables_types",
            canonical_name_vi="Biến, Kiểu dữ liệu cơ bản & Toán tử nhập xuất",
            canonical_name_en="Variables, Primitive Types and I/O",
            synonyms=["biến", "variable", "kiểu dữ liệu", "data type", "int", "float", "str", "bool", "print", "input"],
            bloom_level=1,
            category="syntax",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_operators",
            canonical_name_vi="Toán tử số học, logic và so sánh",
            canonical_name_en="Arithmetic, Comparison and Logical Operators",
            synonyms=["toán tử", "operator", "so sánh", "logic", "and", "or", "not"],
            prerequisites=["python_variables_types"],
            bloom_level=2,
            category="syntax",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_conditionals",
            canonical_name_vi="Cấu trúc rẽ nhánh điều kiện if elif else",
            canonical_name_en="Conditional Statements (if, elif, else)",
            synonyms=["câu lệnh điều kiện", "rẽ nhánh", "if", "elif", "else", "conditional"],
            prerequisites=["python_operators"],
            bloom_level=3,
            category="control_flow",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_loops",
            canonical_name_vi="Vòng lặp for, while và kiểm soát vòng lặp",
            canonical_name_en="Loops (for, while, break, continue)",
            synonyms=["vòng lặp", "loop", "for", "while", "break", "continue", "range"],
            prerequisites=["python_conditionals"],
            bloom_level=3,
            category="control_flow",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_functions",
            canonical_name_vi="Hàm, Tham số, Giá trị trả về và Phạm vi biến",
            canonical_name_en="Functions, Parameters, Return Values and Scope",
            synonyms=["hàm", "function", "def", "return", "tham số", "parameter", "argument", "scope"],
            prerequisites=["python_loops"],
            bloom_level=3,
            category="modular_programming",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_data_structures",
            canonical_name_vi="Cấu trúc dữ liệu có sẵn (List, Tuple, Dictionary, Set)",
            canonical_name_en="Built-in Data Structures (List, Tuple, Dict, Set)",
            synonyms=["danh sách", "list", "từ điển", "dictionary", "dict", "tuple", "set", "cấu trúc dữ liệu"],
            prerequisites=["python_loops", "python_functions"],
            bloom_level=3,
            category="data_structures",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_exceptions",
            canonical_name_vi="Xử lý ngoại lệ và lỗi (try, except, finally)",
            canonical_name_en="Exception Handling (try, except, finally, raise)",
            synonyms=["ngoại lệ", "exception", "try", "except", "finally", "raise", "lỗi runtime"],
            prerequisites=["python_functions"],
            bloom_level=3,
            category="error_handling",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_file_io",
            canonical_name_vi="Đọc ghi tệp tin (File I/O) và Context Manager",
            canonical_name_en="File I/O and Context Managers (with open)",
            synonyms=["đọc file", "ghi file", "file io", "with open", "tệp tin"],
            prerequisites=["python_functions", "python_exceptions"],
            bloom_level=3,
            category="io",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_oop_classes",
            canonical_name_vi="Lập trình hướng đối tượng (OOP) — Lớp & Đối tượng",
            canonical_name_en="Object-Oriented Programming — Classes and Objects",
            synonyms=["lớp và đối tượng", "định nghĩa class", "khởi tạo đối tượng", "class and object", "khái niệm class", "__init__"],
            prerequisites=["python_functions", "python_data_structures"],
            bloom_level=3,
            category="oop",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_oop_inheritance",
            canonical_name_vi="Tính Kế thừa (Inheritance) & Đóng gói (Encapsulation)",
            canonical_name_en="Inheritance and Encapsulation",
            synonyms=["kế thừa", "tính kế thừa", "inheritance", "đóng gói", "encapsulation", "lớp cha", "lớp con"],
            prerequisites=["python_oop_classes"],
            bloom_level=4,
            category="oop",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_oop_polymorphism",
            canonical_name_vi="Tính Đa hình (Polymorphism) & Phương thức trừu tượng",
            canonical_name_en="Polymorphism and Method Overriding",
            synonyms=["đa hình", "tính đa hình", "polymorphism", "ghi đè phương thức", "abstract class", "duck typing"],
            prerequisites=["python_oop_inheritance"],
            bloom_level=4,
            category="oop",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_modules_packages",
            canonical_name_vi="Modules, Packages và Quản lý thư viện pip",
            canonical_name_en="Modules, Packages and Dependency Management (pip)",
            synonyms=["module", "package", "import", "pip", "thư viện"],
            prerequisites=["python_functions"],
            bloom_level=3,
            category="architecture",
            tech_stack="python"
        ),
        OntologyConcept(
            concept_id="python_virtualenv",
            canonical_name_vi="Môi trường ảo (Virtual Environment — venv)",
            canonical_name_en="Virtual Environments (venv)",
            synonyms=["môi trường ảo", "venv", "virtualenv", "virtual environment"],
            prerequisites=["python_modules_packages"],
            bloom_level=2,
            category="tooling",
            tech_stack="python"
        ),
    ]

    for c in concepts:
        graph.add_concept(c)
    return graph


def build_java_ontology() -> CurriculumOntologyGraph:
    graph = CurriculumOntologyGraph(tech_stack="java", domain_name="Java Standard Edition & OOP")

    concepts = [
        OntologyConcept(
            concept_id="java_syntax_types",
            canonical_name_vi="Cú pháp cơ bản, Biến & Kiểu dữ liệu nguyên thủy",
            canonical_name_en="Basic Syntax, Variables and Primitive Types",
            synonyms=["java biến", "kiểu dữ liệu nguyên thủy", "int", "double", "boolean", "system.out.println"],
            bloom_level=1,
            category="syntax",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_control_flow",
            canonical_name_vi="Cấu trúc điều khiển (if-else, switch-case, for, while)",
            canonical_name_en="Control Flow (if-else, switch, for, while)",
            synonyms=["điều khiển luồng", "if else java", "switch case", "vòng lặp java"],
            prerequisites=["java_syntax_types"],
            bloom_level=2,
            category="control_flow",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_methods",
            canonical_name_vi="Phương thức (Methods) và Nạp chồng (Method Overloading)",
            canonical_name_en="Methods, Return Types and Overloading",
            synonyms=["phương thức", "method", "hàm java", "overloading", "nạp chồng phương thức"],
            prerequisites=["java_control_flow"],
            bloom_level=3,
            category="modular_programming",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_oop_classes",
            canonical_name_vi="Lớp, Đối tượng, Hàm tạo (Constructor) và từ khóa this",
            canonical_name_en="Classes, Objects, Constructors and this Keyword",
            synonyms=["class java", "đối tượng java", "constructor", "hàm tạo", "this", "oop java"],
            prerequisites=["java_methods"],
            bloom_level=3,
            category="oop",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_oop_inheritance",
            canonical_name_vi="Kế thừa (extends), từ khóa super và Ghi đè (Override)",
            canonical_name_en="Inheritance, super keyword and Method Overriding",
            synonyms=["kế thừa java", "extends", "super", "override", "@override"],
            prerequisites=["java_oop_classes"],
            bloom_level=4,
            category="oop",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_interfaces",
            canonical_name_vi="Giao diện (Interface) và Lớp trừu tượng (Abstract Class)",
            canonical_name_en="Interfaces and Abstract Classes",
            synonyms=["interface", "giao diện", "abstract class", "lớp trừu tượng", "implements"],
            prerequisites=["java_oop_inheritance"],
            bloom_level=4,
            category="oop",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_collections",
            canonical_name_vi="Java Collections Framework (List, ArrayList, Map, Set)",
            canonical_name_en="Java Collections Framework",
            synonyms=["collections", "arraylist", "hashmap", "hashset", "list java", "map java"],
            prerequisites=["java_oop_classes", "java_interfaces"],
            bloom_level=3,
            category="data_structures",
            tech_stack="java"
        ),
        OntologyConcept(
            concept_id="java_exceptions",
            canonical_name_vi="Xử lý ngoại lệ trong Java (try-catch-finally, throw, throws)",
            canonical_name_en="Exception Handling in Java",
            synonyms=["try catch java", "throw throws", "exception java", "ngoại lệ java"],
            prerequisites=["java_oop_classes"],
            bloom_level=3,
            category="error_handling",
            tech_stack="java"
        ),
    ]

    for c in concepts:
        graph.add_concept(c)
    return graph


def build_sql_ontology() -> CurriculumOntologyGraph:
    graph = CurriculumOntologyGraph(tech_stack="sql", domain_name="Relational Databases & SQL")

    concepts = [
        OntologyConcept(
            concept_id="db_relational_concepts",
            canonical_name_vi="Khái niệm Cơ sở dữ liệu quan hệ, Bảng, Hàng, Cột & Khóa chính",
            canonical_name_en="Relational Concepts, Tables, Primary Key",
            synonyms=["cơ sở dữ liệu", "database", "bảng", "table", "primary key", "khóa chính"],
            bloom_level=1,
            category="foundation",
            tech_stack="sql"
        ),
        OntologyConcept(
            concept_id="sql_ddl_tables",
            canonical_name_vi="Định nghĩa dữ liệu DDL (CREATE TABLE, ALTER, DROP, Ràng buộc)",
            canonical_name_en="Data Definition Language DDL",
            synonyms=["ddl", "create table", "alter table", "drop table", "constraints", "ràng buộc"],
            prerequisites=["db_relational_concepts"],
            bloom_level=3,
            category="ddl",
            tech_stack="sql"
        ),
        OntologyConcept(
            concept_id="sql_dql_select",
            canonical_name_vi="Truy vấn dữ liệu cơ bản (SELECT, FROM, WHERE, ORDER BY)",
            canonical_name_en="Basic Data Querying (SELECT, WHERE, ORDER BY)",
            synonyms=["select", "from", "where", "order by", "truy vấn cơ bản"],
            prerequisites=["sql_ddl_tables"],
            bloom_level=2,
            category="dql",
            tech_stack="sql"
        ),
        OntologyConcept(
            concept_id="sql_aggregate_group_by",
            canonical_name_vi="Hàm tổng hợp (COUNT, SUM, AVG) và Mệnh đề GROUP BY, HAVING",
            canonical_name_en="Aggregate Functions and GROUP BY, HAVING",
            synonyms=["group by", "having", "count", "sum", "avg", "hàm tổng hợp"],
            prerequisites=["sql_dql_select"],
            bloom_level=3,
            category="dql",
            tech_stack="sql"
        ),
        OntologyConcept(
            concept_id="sql_joins",
            canonical_name_vi="Liên kết bảng (INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN)",
            canonical_name_en="Table Joins (INNER, LEFT, RIGHT, FULL JOIN)",
            synonyms=["join", "inner join", "left join", "right join", "liên kết bảng", "khóa ngoại", "foreign key"],
            prerequisites=["sql_dql_select"],
            bloom_level=4,
            category="dql",
            tech_stack="sql"
        ),
        OntologyConcept(
            concept_id="sql_subqueries",
            canonical_name_vi="Truy vấn con (Subqueries / Nested Queries)",
            canonical_name_en="Subqueries and Nested Queries",
            synonyms=["subquery", "nested query", "truy vấn con"],
            prerequisites=["sql_joins", "sql_aggregate_group_by"],
            bloom_level=4,
            category="dql",
            tech_stack="sql"
        ),
        OntologyConcept(
            concept_id="sql_transactions_acid",
            canonical_name_vi="Giao dịch cơ sở dữ liệu (Transaction) & Tính chất ACID",
            canonical_name_en="Database Transactions and ACID Properties",
            synonyms=["transaction", "giao dịch", "commit", "rollback", "acid"],
            prerequisites=["sql_ddl_tables"],
            bloom_level=4,
            category="advanced",
            tech_stack="sql"
        ),
    ]

    for c in concepts:
        graph.add_concept(c)
    return graph


def build_agile_ontology() -> CurriculumOntologyGraph:
    graph = CurriculumOntologyGraph(tech_stack="agile", domain_name="Agile & Scrum Methodology")

    concepts = [
        OntologyConcept(
            concept_id="agile_manifesto",
            canonical_name_vi="Tuyên ngôn Agile & 4 Giá trị cốt lõi, 12 Nguyên tắc",
            canonical_name_en="Agile Manifesto, 4 Core Values and 12 Principles",
            synonyms=["agile", "tuyên ngôn agile", "agile manifesto", "triết lý agile"],
            bloom_level=1,
            category="foundation",
            tech_stack="agile"
        ),
        OntologyConcept(
            concept_id="scrum_framework_roles",
            canonical_name_vi="Khung làm việc Scrum & 3 Vai trò (PO, SM, Dev Team)",
            canonical_name_en="Scrum Framework and 3 Roles (PO, Scrum Master, Developers)",
            synonyms=["scrum", "product owner", "scrum master", "developer", "vai trò scrum"],
            prerequisites=["agile_manifesto"],
            bloom_level=2,
            category="roles",
            tech_stack="agile"
        ),
        OntologyConcept(
            concept_id="scrum_artifacts",
            canonical_name_vi="3 Tạo tác Scrum (Product Backlog, Sprint Backlog, Increment)",
            canonical_name_en="Scrum Artifacts (Product Backlog, Sprint Backlog, Increment)",
            synonyms=["product backlog", "sprint backlog", "increment", "tạo tác scrum", "artifact"],
            prerequisites=["scrum_framework_roles"],
            bloom_level=2,
            category="artifacts",
            tech_stack="agile"
        ),
        OntologyConcept(
            concept_id="user_stories_invest",
            canonical_name_vi="User Story, Phân rã Epic, Tiêu chuẩn INVEST & Acceptance Criteria",
            canonical_name_en="User Stories, INVEST Criteria and Acceptance Criteria",
            synonyms=["user story", "invest", "acceptance criteria", "gherkin", "epic", "dod", "dor"],
            prerequisites=["scrum_artifacts"],
            bloom_level=3,
            category="requirements",
            tech_stack="agile"
        ),
        OntologyConcept(
            concept_id="estimation_planning_poker",
            canonical_name_vi="Ước lượng Story Points & Kỹ thuật Planning Poker",
            canonical_name_en="Estimation, Story Points and Planning Poker",
            synonyms=["story point", "planning poker", "ước lượng", "estimation", "fibonacci"],
            prerequisites=["user_stories_invest"],
            bloom_level=3,
            category="planning",
            tech_stack="agile"
        ),
        OntologyConcept(
            concept_id="sprint_execution_burndown",
            canonical_name_vi="Vận hành Sprint, Daily Scrum & Theo dõi Burndown Chart",
            canonical_name_en="Sprint Execution, Daily Scrum and Burndown Chart",
            synonyms=["sprint", "daily scrum", "burndown chart", "sprint planning", "vận hành sprint"],
            prerequisites=["estimation_planning_poker"],
            bloom_level=3,
            category="execution",
            tech_stack="agile"
        ),
        OntologyConcept(
            concept_id="sprint_review_retro",
            canonical_name_vi="Sprint Review (Demo) & Sprint Retrospective (Cải tiến liên tục)",
            canonical_name_en="Sprint Review and Sprint Retrospective",
            synonyms=["sprint review", "retrospective", "retro", "cải tiến quy trình", "demo sản phẩm"],
            prerequisites=["sprint_execution_burndown"],
            bloom_level=4,
            category="continuous_improvement",
            tech_stack="agile"
        ),
    ]

    for c in concepts:
        graph.add_concept(c)
    return graph


# Pre-built Ontology Registry
_ONTOLOGY_REGISTRY: Dict[str, CurriculumOntologyGraph] = {
    "python": build_python_ontology(),
    "java": build_java_ontology(),
    "sql": build_sql_ontology(),
    "database": build_sql_ontology(),
    "agile": build_agile_ontology(),
    "scrum": build_agile_ontology(),
}


def get_ontology_for_stack(tech_stack: str) -> Optional[CurriculumOntologyGraph]:
    """
    Retrieves the standard ontology graph for a given technology stack.
    Matches case-insensitively by keyword.
    """
    if not tech_stack:
        return None
    stack_lower = tech_stack.lower().strip()
    for key, ontology in _ONTOLOGY_REGISTRY.items():
        if key in stack_lower:
            return ontology
    return None
