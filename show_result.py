import markdown
from driver import SeleniumDriverSingleton

def show_markdown_popup(driver, markdown_text):
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_text)

    # Escape backticks or backslashes in the HTML string to safely embed in JS
    escaped_html = html_content.replace("`", "\\`").replace("\\", "\\\\")

    js_code = f"""
    const existing = document.getElementById('markdownModal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'markdownModal';
    modal.innerHTML = `
        <div style="
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            font-family: Arial, sans-serif;
        ">
            <div style="
                background: #fff;
                padding: 25px 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 90%;
                box-sizing: border-box;
                color: #333;
                line-height: 1.5;
                overflow-y: auto;
                max-height: 80vh;
            ">
                <div style="max-height: 70vh; overflow-y: auto;">${escaped_html}</div>
                <div style="text-align: center; margin-top: 20px;">
                    <button
                        onclick="document.getElementById('markdownModal').remove();"
                        style="
                            padding: 10px 20px;
                            font-size: 15px;
                            background-color: #4CAF50;
                            border: none;
                            color: white;
                            border-radius: 5px;
                            cursor: pointer;
                        "
                    >Close</button>
                </div>
            </div>
        </div>`;
    document.body.appendChild(modal);
    """

    driver.get_driver().execute_script(js_code)

if __name__ == "__main__":
    driver = SeleniumDriverSingleton()
    driver.access_web_page("https://www.delhaize.be/")

    markdown_text = """
    # How may I help you?

    **Ingredients:**

    - 500g minced beef
    - 1 onion
    - 400g canned tomatoes

    **Instructions:**

    Fry onions and beef. Add tomatoes and simmer for 20 minutes.

    [Watch the video](https://www.youtube.com/watch?v=-gF8d-fitkU)
    """
    show_markdown_popup(driver, markdown_text)
    input("Press Enter to close browser and end script...")
else:
    print(f"Importing module: {__name__}...")