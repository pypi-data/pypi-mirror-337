import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from create_graph import build_dependency_graph, visualize_dependency_graph
from level_segregation import segregate_levels
import multiprocessing

def extract_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# def process_node(node, project_root, dependencies):
#     sanitized_file_name = node.replace("\\/", "\/")
#     full_path = os.path.join(project_root, sanitized_file_name)
#     file_content = extract_text_from_file(full_path)
    
#     if not file_content:
#         return f"Failed to process {node}"

#     prompt = f"""{file_content}You are a technical writer tasked with creating code documentation for this particular 
#     code file in the Engineering department of a technology/software company. 
#     Write a function-by-function overview explaining key tasks, purpose, and aspects, and defining 
#     segments of each function. Follow consistent formatting, use clear and concise language, provide context 
#     where necessary. Keep in mind, that this code file is a part of a much larger software project.
#     Since this code file is part of a larger software project, the functions used may be defined in other 
#     files or dependencies. 
#     generate a markdown documentation for this current file: {node}. Return only the markdown part 
#     of the documentation. Do not include any other text or explanation. No ''''markdown tag or anything."""

#     client = OpenAI()
#     client.api_key = os.getenv("OPENAI_API_KEY")
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )
    
#     docs_dir = os.path.join(os.getcwd(), "generated_docs")
#     os.makedirs(docs_dir, exist_ok=True)
#     doc_path = os.path.join(docs_dir, f"{node[:-3]}.md")
#     with open(doc_path, "w", encoding="utf-8") as f:
#         f.write(response.choices[0].message.content.strip())

#     dependent_nodes = dependencies.get(node, {})
#     dependent_functions = {dep_node: functions for dep_node, functions in dependent_nodes.items()}
    
#     return f"Processed {node}"

# Global storage for function summaries:
node_function_summaries = {}  # { parent_node: { function_name: summary } }

def process_node(node, project_root, dependencies):
    print(f"Processing node: {node}")
    sanitized_file_name = node.replace("\\/", "\/")
    full_path = os.path.join(project_root, sanitized_file_name)
    file_content = extract_text_from_file(full_path)
    
    if not file_content:
        return f"Failed to process {node}"
    
    if node_function_summaries and node in node_function_summaries:
        functions = {}
        
        for func in node_function_summaries[node].keys():
            functions[func] = node_function_summaries[node][func]
        
        prompt = f"""{file_content}
        You are a technical writer tasked with creating code documentation for this particular 
        code file in the Engineering department of a technology/software company. 
        Write a function-by-function overview explaining key tasks, purpose, and aspects, and defining 
        segments of each function. Follow consistent formatting, use clear and concise language, provide context 
        where necessary. Keep in mind, that this code file is a part of a much larger software project.
        Since this code file is part of a larger software project, the functions used may be defined in other 
        files or dependencies. Here is a list of functions that have been defined outside the current codefile 
        and their summaries:
        {functions}
        Use these summaries to help you understand the context of the current file.
        generate a markdown documentation for this current file: {node}. Return only the markdown part 
        of the documentation. Do not include any other text or explanation. No ''''markdown tag or anything."""
    
    else:
    # Create documentation for the current node file
        prompt = f"""{file_content}
        You are a technical writer tasked with creating code documentation for this particular 
        code file in the Engineering department of a technology/software company. 
        Write a function-by-function overview explaining key tasks, purpose, and aspects, and defining 
        segments of each function. Follow consistent formatting, use clear and concise language, provide context 
        where necessary. Keep in mind, that this code file is a part of a much larger software project.
        Since this code file is part of a larger software project, the functions used may be defined in other 
        files or dependencies. 
        generate a markdown documentation for this current file: {node}. Return only the markdown part 
        of the documentation. Do not include any other text or explanation. No ''''markdown tag or anything."""
    

    history = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )
    
    history.append(response.choices[0].message)

    # Save the documentation
    docs_dir = os.path.join(os.getcwd(), "generated_docs")
    os.makedirs(docs_dir, exist_ok=True)
    doc_path = os.path.join(docs_dir, f"{node[:-3]}.md")
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(response.choices[0].message.content.strip())
    
    # Find parents in the dependency graph that depend on the current node.
    # For example, given Dependencies: {'task_manager.py': {'storage.py': {'load_tasks', 'save_tasks'}, ...}, ...}
    dependents = {}  # { parent_node: set(functions) }
    for parent_node, child_mapping in dependencies.items():
        if node in child_mapping:
            dependents[parent_node] = child_mapping[node]
    
    # For every parent dependent, query the agent for a summary of each used function.
    if dependents:
        for parent, functions in dependents.items():
            func_summaries_for_parent = {}
            for func in functions:
                func_prompt = (
                    f"For the file {node}"
                    f"Please provide a summary for the function '{func}' including: "
                    "1) its input parameters, 2) its output parameters, and 3) the role it plays as used by "
                )
                history.append({
                    "role": "user",
                    "content": func_prompt
                })
                response_func = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=history
                )
                history.append(response_func.choices[0].message)
                summary_text = response_func.choices[0].message.content.strip()
                func_summaries_for_parent[func] = summary_text
            if node_function_summaries.get(parent) is None:
                node_function_summaries[parent] = func_summaries_for_parent
            else:
                node_function_summaries[parent].update(func_summaries_for_parent)

    return f"Processed {node}"

def main():
    project_root = input("Enter the project root directory: ").strip()
    if not os.path.isdir(project_root):
        print("Invalid directory. Please check the path.")
        return
    graph = build_dependency_graph(project_root)
    print("Nodes:", graph.nodes)
    print("Edges:", graph.edges)
    visualize_dependency_graph(graph)

    print(graph)

    # Get Levels
    levels, dependencies = segregate_levels(graph)

    print("Levels:", levels)
    print("Dependencies:", dependencies)
    
    for level in levels:
        print(f"Processing level {level} ...")
        curr_level = list(levels[level])

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_node, node, project_root, dependencies) for node in curr_level]
            for future in as_completed(futures):
                print(future.result())
        print(f"Completed processing level {level}.")

if __name__ == "__main__":
    main()

