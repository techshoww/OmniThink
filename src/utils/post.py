import re
import json

def extract_citations(file_path):
    citations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
            citation_matches = re.findall(r'\[\d+\]', content)
            
            citations = [int(match.strip('[]')) for match in citation_matches]
            
            citations = sorted(set(citations))
            
    except FileNotFoundError:
        print(f"{file_path} not found.")
    except Exception as e:
        print(f"error:{e}")
    
    return citations

def load_map(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    mymap = {}
    for url in data['url_to_unified_index'].keys():
        index = data['url_to_unified_index'][url]
        mymap[index] = url
    return mymap

def remove_lines_after_marker(content: str, marker: str = '---') -> str:
    """
    Remove the line immediately following the marker in the content.
    """
    lines = content.splitlines()
    updated_lines = []
    skip_next_line = False
    
    for line in lines:
        if skip_next_line:
            skip_next_line = False
            continue
        if line.strip() == marker:
            skip_next_line = True
        else:
            updated_lines.append(line)
    
    return '\n'.join(updated_lines)

def add_ref(citations, mymap, content):
    references = "\n\n参考文献:\n"
    for citation in citations:
        if citation in mymap:
            references += f"[{citation}] {mymap[citation]}\n"
        else:
            references += f"[{citation}] 未找到对应的URL\n"
    
    content += references
    return content

def polish(article_path, map_path):
    citations = extract_citations(article_path)
    mymap = load_map(map_path)

    with open(article_path, 'r', encoding='utf-8') as file:
        content = file.read()
  
    content = add_ref(citations, mymap, content)
    content = remove_lines_after_marker(content, marker='---')
    content = remove_consecutive_duplicate_citations(content)
        
    with open(article_path, 'w', encoding='utf-8') as file:
        file.write(content)    
        print("参考文献已成功附加到文章末尾。")
    

def remove_consecutive_duplicate_citations(content: str) -> str:
    """
    This function removes consecutive duplicate citations in the text within the same line,
    deleting earlier instances and keeping only the last one when duplicates are adjacent.
    """
    # Split the content into lines
    lines = content.splitlines()
    
    processed_lines = []
    
    for line in lines:
        # Find all citations and split them from the text
        parts = re.split(r'(\[\d+\])', line)
        
        # List to hold the new parts after removing duplicates
        new_parts = []
        last_citation = None
        last_citation_index = -1
        
        for index, part in enumerate(parts):
            if re.match(r'\[\d+\]', part):
                if part == last_citation:
                    # If the current citation is the same as the last, remove the last one
                    new_parts.pop(last_citation_index)
                last_citation = part
                last_citation_index = len(new_parts)
            new_parts.append(part)
        
        # Reconstruct the line, ensuring we remove any trailing empty parts
        new_line = ''.join([p for p in new_parts if p != ''])
        processed_lines.append(new_line)
    
    # Join the processed lines back into a single string
    return '\n'.join(processed_lines)


  

if __name__ == '__main__':
    # path = '/mnt/nas-alinlp/xizekun/project/storm/results/gpt/台风玛莉亚'
    # article_path = path + '/storm_gen_article_polished.txt'
    # map_path = path + '/url_to_info.json'
    # # 调用函数将参考文献添加到文章末尾
    # append_references_to_article(article_path, map_path)


    string = "你好[1]你好[2]你好啊[1]你非常好[1]你非常的好[1]你非常的好[1]你非常的好[1]你好[2]"
    post_string = remove_consecutive_duplicate_citations(string)
    print(post_string)
