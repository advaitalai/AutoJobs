# Takes a job board and parses it to create a list of jobs
# Uses the Job object with incomplete parameters

from bs4 import element
from bs4 import BeautifulSoup
import requests, re

url = 'https://miro.com/careers/open-positions/'
response = requests.get(url)

# This is from accel jobs
test_html = """<div class="jobs_row" oncontextmenu="HandleRightClick('jobdetail.php?jobid=2293017')" data-href="jobdetail.php?jobid=2293017" data-toggle="modal" data-target="#myModal" onclick="ga('send','pageview','Job/Sr. Product Manager (Remote)');return jobdetail('2293017');">
		<div class="jobs_topRow">
			<div class="jobs_descriptionBx">
				<div class="jobs_logo">
					<img class="joblist-logo" src="https://s3.amazonaws.com/media.ventureloop.com/images/Hashnode_paint.png" alt="image">
				</div>
				<div class="job_text">
					<h3>Sr. Product Manager (Remote)</h3>
					<h4><span>Hashnode - </span> Remote</h4>
				</div>
			</div>
			<div class="post_dates">
               <h5>Posted 
                  Today
                  <!-- this is a comment -->               	
               </h5>
			</div>
		</div>
		<div class="jobs_btnnRow">
			<div class="contact_info">
				<div class="attached_icon">
				</div>
                        <div class="info_text">
                                <h5>Industry: <span>Cloud/SaaS</span></h5>
                                <h5>Employment Type: <span>Full-Time</span></h5>
                        </div>

			</div>
			<div class="apply_btnbx">
				<div class="upload_bxInnr">
				<!--<div class="bookmark_btn">
					<a href="jabvascript:void(0)">
						<svg viewBox="0 0 384 512"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#bookmark_icon"></use></svg>   
					</a>
				</div>-->
				<div class="upload_btn">
											<a href="jobdetail.php?jobid=2293017">See Details</a>												</div>
			</div>
			</div>
		</div>
	</div>"""

soup = BeautifulSoup(test_html, 'html.parser')

# Algo is as follows
# 1. Find the first occurence of a title
# 2. Add sibling leaves to the appropriate dict key (e.g. location)
# 3. Move up the parent and find more leaves from different trees until a new title is encountered.
# 4. If the current title was a singleton attribute, delete this job. 

title_count = 0
match_found = 0
    
def traverse_job_attributes(tag: element.Tag) -> None:
    ''' Takes a leaf title tag and prints all other attributes bottoms-up until it hits another title tag '''
    
    # If tag has no parent, return
    if tag.parent is None:
        return
    
    global title_count
    print("Tag is now ", tag.name)
    
    # Do nothing if comment
    if isinstance(tag, element.Comment):
        return
    
    # Print leaf nodes except the second title. Parents will never be leaf nodes and hence not printed. 
    if is_leaf_tag(tag):
        leaf_str = str(tag.string)
        
        if 'Product' in leaf_str:
            title_count = title_count + 1
            
        # Check if we've encountered a second title, do not print if so
        if title_count == 2:
            title_count = 0 # reset the title count
            return
            
        print(leaf_str)
    
    # print all sibling leaves
    for ns in tag.next_siblings:
        print("Printing next siblings of ", tag.name)
        print_leaves(ns)
        
    for ps in tag.previous_siblings:
        print("Printing previous siblings of ", tag.name)
        print_leaves(ps)
        
    # Move to the parent and do the same
    traverse_job_attributes(tag.parent)
    

def print_leaves(tag: element.Tag, escape_str: re.Pattern) -> None:
    ''' Prints all the nodes of the tree from the tag below, inclusive. Escapes if it finds the escape string 
        in any of the tag children 
    '''
    global match_found
    
    # Print if the tag is a leaf
    if is_leaf_tag(tag):
        print(tag)
        return
    
    # Return if it finds a regex match
    if is_matched_leaf(tag, escape_str):
        print("Match found! Exiting print_leaves")
        match_found = 1
        return
    
    for child in tag.children:
        print_leaves(child, escape_str)
        
        # Break out if it finds the next role
        if match_found:
            match_found = 0
            return
    

def is_leaf_string(soup_object) -> bool:
    return isinstance(soup_object, element.NavigableString) and len(soup_object.contents) == 0

def is_matched_leaf(tag: element.Tag, check_str: re.Pattern) -> bool:
    return is_leaf_tag(tag) and re.search(check_str, tag.string)

def get_product_tag():
    for tag in soup.find_all():
        if not tag.find_all() and tag.name != 'br' and tag.get_text().lower().find('product') != -1:
            return tag
    return None
        
def has_regex(pattern: re.Pattern, body: str) -> bool:
    match = re.search(pattern, body)
    if match:
        return True
    else:
        return False

# 1. Print tag if string
# 2. Print left sibling trees
# 3. Print right siblings
# 4. Recurse on parent
# 5. Break when regex is found

def print_tree(tag, escape_re: re.Pattern) -> None:
    
    # Print if the tag is a string
    if isinstance(tag, element.NavigableString):
        print(tag)
        
    # Exit if we find an escape match
    
    # Print descendants if any
    
    # Print siblings
    
#test_tag = find_product_leaf()
#pattern = re.compile(r'product', re.IGNORECASE)
#print(test_tag)
#print_leaves(soup.find('html'), pattern)
#traverse_job_attributes(test_tag)