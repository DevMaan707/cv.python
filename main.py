import json
import os
import datetime
import sys
from pathlib import Path

def get_input(prompt, multiline=False, required=True):
    """Get user input with support for multiline text"""
    print(prompt)
    if multiline:
        print("(Enter an empty line to finish)")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        value = "\n".join(lines)
    else:
        value = input()

    if required and not value:
        print("This field is required. Please enter a value.")
        return get_input(prompt, multiline, required)

    return value

def collect_user_data():
    """Collect all user information for the CV"""
    data = {}
    print("\n=== PERSONAL INFORMATION ===")
    data['personal'] = {
        'name': get_input("Enter your full name:"),
        'title': get_input("Enter your professional title:"),
        'email': get_input("Enter your email:"),
        'phone': get_input("Enter your phone number:"),
        'location': get_input("Enter your location:"),
        'website': get_input("Enter your website/portfolio URL:", required=False),
        'linkedin': get_input("Enter your LinkedIn URL:", required=False),
        'github': get_input("Enter your GitHub URL:", required=False),
        'twitter': get_input("Enter your Twitter URL:", required=False),
        'summary': get_input("Enter a professional summary:", multiline=True)
    }
    print("\n=== WORK EXPERIENCE ===")
    data['experience'] = []

    while True:
        print("\nAdd a work experience entry (or leave title empty to finish):")
        title = get_input("Job Title:", required=False)
        if not title:
            break

        company = get_input("Company Name:")
        location = get_input("Location:")
        start_date = get_input("Start Date (e.g. Jan 2020):")
        end_date = get_input("End Date (e.g. Present):")
        description = get_input("Job Description:", multiline=True)

        data['experience'].append({
            'title': title,
            'company': company,
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'description': description
        })
    print("\n=== EDUCATION ===")
    data['education'] = []

    while True:
        print("\nAdd an education entry (or leave degree empty to finish):")
        degree = get_input("Degree:", required=False)
        if not degree:
            break

        institution = get_input("Institution:")
        location = get_input("Location:")
        start_date = get_input("Start Date (e.g. Sep 2015):")
        end_date = get_input("End Date (e.g. Jun 2019):")
        description = get_input("Description (optional):", multiline=True, required=False)

        data['education'].append({
            'degree': degree,
            'institution': institution,
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'description': description
        })
    print("\n=== SKILLS ===")
    data['skills'] = []
    print("Enter your skills (one skill per line, empty line to finish):")
    while True:
        skill = input()
        if not skill:
            break
        data['skills'].append(skill)
    print("\n=== PROJECTS ===")
    data['projects'] = []

    while True:
        print("\nAdd a project (or leave name empty to finish):")
        name = get_input("Project Name:", required=False)
        if not name:
            break

        url = get_input("Project URL:", required=False)
        description = get_input("Description:", multiline=True)
        technologies = get_input("Technologies used (comma-separated):")

        data['projects'].append({
            'name': name,
            'url': url,
            'description': description,
            'technologies': [tech.strip() for tech in technologies.split(',')]
        })
    print("\n=== LANGUAGES ===")
    data['languages'] = []

    while True:
        print("\nAdd a language (or leave language empty to finish):")
        language = get_input("Language:", required=False)
        if not language:
            break

        proficiency = get_input("Proficiency (e.g. Native, Fluent, Intermediate, Basic):")

        data['languages'].append({
            'language': language,
            'proficiency': proficiency
        })
    print("\n=== CERTIFICATIONS ===")
    data['certifications'] = []

    while True:
        print("\nAdd a certification (or leave name empty to finish):")
        name = get_input("Certification Name:", required=False)
        if not name:
            break

        issuer = get_input("Issuing Organization:")
        date = get_input("Date (e.g. Jun 2021):")
        url = get_input("URL (optional):", required=False)

        data['certifications'].append({
            'name': name,
            'issuer': issuer,
            'date': date,
            'url': url
        })
    print("\n=== INTERESTS/HOBBIES ===")
    print("Enter your interests or hobbies (one per line, empty line to finish):")
    data['interests'] = []
    while True:
        interest = input()
        if not interest:
            break
        data['interests'].append(interest)

    return data

def save_json(data, filename="cv_data.json"):
    """Save the user data as JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nData saved to {filename}")
    return filename

def load_json(file_path):
    """Load data from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded data from {file_path}")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def generate_cv_html(data, template_path, output_filename):
    """Generate HTML CV from template and data"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Replace personal information
        for key, value in data['personal'].items():
            placeholder = f"{{{{personal.{key}}}}}"
            if isinstance(value, str):
                template = template.replace(placeholder, value)

        # Current date information
        now = datetime.datetime.now()
        template = template.replace("{{current_year}}", str(now.year))
        template = template.replace("{{current_month}}", now.strftime("%B"))

        # Experience items
        experience_html = ""
        if 'experience' in data and data['experience']:
            for exp in data['experience']:
                experience_html += f"""
                <div class="timeline-item">
                    <div class="timeline-header">
                        <h3 class="timeline-title">{exp['title']}</h3>
                        <div class="timeline-date">{exp['start_date']} - {exp['end_date']}</div>
                    </div>
                    <div class="timeline-subtitle">{exp['company']}</div>
                    <div class="timeline-location">📍 {exp['location']}</div>
                    <div class="timeline-content">{exp['description'].replace('\n', '<br>')}</div>
                </div>
                """
        template = template.replace("{{experience_items}}", experience_html)

        # Education items
        education_html = ""
        if 'education' in data and data['education']:
            for edu in data['education']:
                description = f"<div class='timeline-content'>{edu['description'].replace('\n', '<br>')}</div>" if edu.get('description') else ""
                education_html += f"""
                <div class="timeline-item">
                    <div class="timeline-header">
                        <h3 class="timeline-title">{edu['degree']}</h3>
                        <div class="timeline-date">{edu['start_date']} - {edu['end_date']}</div>
                    </div>
                    <div class="timeline-subtitle">{edu['institution']}</div>
                    <div class="timeline-location">📍 {edu['location']}</div>
                    {description}
                </div>
                """
        template = template.replace("{{education_items}}", education_html)

        # Skills
        skills_html = ""
        if 'skills' in data and data['skills']:
            for skill in data['skills']:
                skills_html += f'<div class="skill-tag">{skill}</div>'
        template = template.replace("{{skill_items}}", skills_html)

        # Projects
        projects_html = ""
        if 'projects' in data and data['projects']:
            for project in data['projects']:
                project_title = project['name']
                project_link = f"<a href='{project['url']}' target='_blank'>{project_title}</a>" if project.get('url') else project_title
                tech_tags = ""
                if 'technologies' in project:
                    for tech in project['technologies']:
                        tech_tags += f'<div class="project-tag">{tech}</div>'

                projects_html += f"""
                <div class="project-card">
                    <div class="project-header">
                        <h3 class="project-title">{project_link}</h3>
                    </div>
                    <div class="project-description">{project['description'].replace('\n', '<br>')}</div>
                    <div class="project-tags">{tech_tags}</div>
                </div>
                """
        template = template.replace("{{project_items}}", projects_html)

        # Languages
        languages_html = ""
        if 'languages' in data and data['languages']:
            for lang in data['languages']:
                languages_html += f"""
                <div class="language-card">
                    <div class="language-info">
                        <div class="language-name">{lang['language']}</div>
                        <div class="language-level">{lang['proficiency']}</div>
                    </div>
                    <div class="language-badge">{lang['proficiency']}</div>
                </div>
                """
        template = template.replace("{{language_items}}", languages_html)

        # Certifications
        certifications_html = ""
        if 'certifications' in data and data['certifications']:
            for cert in data['certifications']:
                cert_name = cert['name']
                cert_link = f"<a href='{cert['url']}' target='_blank'>{cert_name}</a>" if cert.get('url') else cert_name
                certifications_html += f"""
                <div class="certification-card">
                    <div class="certification-name">{cert_link}</div>
                    <div class="certification-meta">
                        <span>{cert['issuer']}</span>
                        <span>{cert['date']}</span>
                    </div>
                </div>
                """
        template = template.replace("{{certification_items}}", certifications_html)

        # Interests
        interests_html = ""
        if 'interests' in data and data['interests']:
            for interest in data['interests']:
                interests_html += f'<div class="interest-item">{interest}</div>'
        template = template.replace("{{interest_items}}", interests_html)

        # Create output directory if it doesn't exist
        output_dir = Path("generated_cvs")
        output_dir.mkdir(exist_ok=True)

        # Write the output file
        output_path = output_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)

        return output_path

    except Exception as e:
        print(f"Error generating CV: {e}")
        return None

def process_json_file(json_path):
    """Process a JSON file and generate CVs from its data"""
    data = load_json(json_path)
    if not data:
        return False

    # Get base filename without extension
    base_name = Path(json_path).stem

    # Find available templates
    templates_dir = Path(".")
    template_files = list(templates_dir.glob("template*.html"))

    if not template_files:
        print("No template files found. Please ensure template files (template1.html, etc.) are in the current directory.")
        return False

    success_count = 0
    for template_path in template_files:
        template_name = template_path.stem
        output_filename = f"{base_name}_{template_name}.html"

        output_path = generate_cv_html(data, template_path, output_filename)
        if output_path:
            print(f"CV generated at: {output_path}")
            success_count += 1

    print(f"\nSuccessfully generated {success_count} CV templates from {json_path}")
    return success_count > 0

def process_directory(dir_path):
    """Process all JSON files in a directory"""
    try:
        dir_path = Path(dir_path)
        if not dir_path.is_dir():
            print(f"Error: {dir_path} is not a valid directory.")
            return False

        json_files = list(dir_path.glob("*.json"))
        if not json_files:
            print(f"No JSON files found in {dir_path}")
            return False

        success_count = 0
        for json_file in json_files:
            print(f"\nProcessing {json_file.name}...")
            if process_json_file(json_file):
                success_count += 1

        print(f"\nSuccessfully processed {success_count} out of {len(json_files)} JSON files.")
        return success_count > 0

    except Exception as e:
        print(f"Error processing directory: {e}")
        return False

def main():
    print("=== Professional CV Generator ===")

    # Main menu for input method selection
    while True:
        print("\nHow would you like to input your CV data?")
        print("1. Enter data interactively")
        print("2. Use a JSON file")
        print("3. Process a directory of JSON files")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            # Interactive data collection
            try:
                data = collect_user_data()
                filename = save_json(data)

                # Generate CVs from the collected data
                templates_dir = Path(".")
                template_files = list(templates_dir.glob("template*.html"))

                if not template_files:
                    print("No template files found. Please ensure template files (template1.html, etc.) are in the current directory.")
                    continue

                success_count = 0
                for template_path in template_files:
                    template_name = template_path.stem
                    output_filename = f"{Path(filename).stem}_{template_name}.html"

                    output_path = generate_cv_html(data, template_path, output_filename)
                    if output_path:
                        print(f"CV generated at: {output_path}")
                        success_count += 1

                if success_count > 0:
                    print(f"\nSuccessfully generated {success_count} CV templates in the 'generated_cvs' directory!")
                    print("You can open these HTML files in your web browser to view and print them.")
                else:
                    print("\nFailed to generate any CV templates. Please check the error messages above.")

            except KeyboardInterrupt:
                print("\n\nCV generation interrupted. Your progress may not be fully saved.")
                continue
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                continue

        elif choice == "2":
            # Process a single JSON file
            json_path = input("\nEnter the path to your JSON file: ").strip()
            process_json_file(json_path)

        elif choice == "3":
            # Process a directory of JSON files
            dir_path = input("\nEnter the directory path containing JSON files: ").strip()
            process_directory(dir_path)

        elif choice == "4":
            print("\nExiting CV Generator. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
