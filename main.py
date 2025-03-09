
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

def generate_cv_html(data, template_number=1):
    """Generate HTML CV from template and data"""
    try:
        template_file = f"template{template_number}.html"
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        for key, value in data['personal'].items():
            template = template.replace(f"{{{{personal.{key}}}}}", value)
        experience_html = ""
        for exp in data['experience']:
            experience_html += f"""
            <div class="experience-item">
                <h3>{exp['title']}</h3>
                <div class="company-details">
                    <h4>{exp['company']}</h4>
                    <div class="location-date">
                        <span>{exp['location']}</span>
                        <span>{exp['start_date']} - {exp['end_date']}</span>
                    </div>
                </div>
                <div class="job-description">
                    <p>{exp['description'].replace('\n', '<br>')}</p>
                </div>
            </div>
            """
        template = template.replace("{{experience_items}}", experience_html)
        education_html = ""
        for edu in data['education']:
            description = f"<p>{edu['description'].replace('\n', '<br>')}</p>" if edu['description'] else ""
            education_html += f"""
            <div class="education-item">
                <h3>{edu['degree']}</h3>
                <div class="institution-details">
                    <h4>{edu['institution']}</h4>
                    <div class="location-date">
                        <span>{edu['location']}</span>
                        <span>{edu['start_date']} - {edu['end_date']}</span>
                    </div>
                </div>
                <div class="education-description">
                    {description}
                </div>
            </div>
            """
        template = template.replace("{{education_items}}", education_html)
        skills_html = ""
        for skill in data['skills']:
            skills_html += f'<span class="skill-item">{skill}</span>'
        template = template.replace("{{skill_items}}", skills_html)
        projects_html = ""
        for project in data['projects']:
            project_title = f"<a href='{project['url']}'>{project['name']}</a>" if project['url'] else project['name']
            tech_html = " ".join([f"<span class='tech-tag'>{tech}</span>" for tech in project['technologies']])

            projects_html += f"""
            <div class="project-item">
                <h3>{project_title}</h3>
                <div class="project-description">
                    <p>{project['description'].replace('\n', '<br>')}</p>
                </div>
                <div class="technologies">
                    {tech_html}
                </div>
            </div>
            """
        template = template.replace("{{project_items}}", projects_html)
        languages_html = ""
        for lang in data['languages']:
            languages_html += f"""
            <div class="language-item">
                <span class="language-name">{lang['language']}</span>
                <span class="language-level">{lang['proficiency']}</span>
            </div>
            """
        template = template.replace("{{language_items}}", languages_html)
        certifications_html = ""
        for cert in data['certifications']:
            cert_name = f"<a href='{cert['url']}'>{cert['name']}</a>" if cert['url'] else cert['name']
            certifications_html += f"""
            <div class="certification-item">
                <h4>{cert_name}</h4>
                <div class="certification-details">
                    <span>{cert['issuer']}</span>
                    <span>{cert['date']}</span>
                </div>
            </div>
            """
        template = template.replace("{{certification_items}}", certifications_html)
        interests_html = ""
        for interest in data['interests']:
            interests_html += f'<span class="interest-item">{interest}</span>'
        template = template.replace("{{interest_items}}", interests_html)
        current_year = datetime.datetime.now().year
        template = template.replace("{{current_year}}", str(current_year))
        output_dir = Path("generated_cvs")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"cv_template{template_number}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)

        print(f"CV generated at: {output_path}")
        return True

    except FileNotFoundError:
        print(f"Template file template{template_number}.html not found.")
        return False
    except Exception as e:
        print(f"Error generating CV from template {template_number}: {e}")
        return False

def main():
    print("=== Professional CV Generator ===")
    print("\nThis program will guide you through creating professional CV templates.")
    print("Let's collect information for your CV. Fill out each section carefully.")

    try:
        data = collect_user_data()
        save_json(data)
        print("\nGenerating your CV templates...")
        success_count = 0
        for i in range(1, 4):
            if generate_cv_html(data, i):
                success_count += 1
        if success_count > 0:
            print(f"\nSuccessfully generated {success_count} CV templates in the 'generated_cvs' directory!")
            print("You can open these HTML files in your web browser to view and print them.")
        else:
            print("\nFailed to generate any CV templates. Please check the error messages above.")
    except KeyboardInterrupt:
        print("\n\nCV generation interrupted. Your progress has not been saved.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
