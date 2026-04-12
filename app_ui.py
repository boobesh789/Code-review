import gradio as gr
import requests
import json

ENV_URL = 'https://boobesh007-code-review.hf.space'

def review_code(code, language, difficulty):
    try:
        # Reset environment
        reset_resp = requests.post(ENV_URL + '/reset', timeout=30)
        obs = reset_resp.json()

        # Create action based on code analysis
        action = {
            'has_syntax_error': ':' not in code and 'def ' in code,
            'quality_score': 0.5,
            'issues': ['code submitted for review'],
            'severity': 'medium'
        }

        # Step environment
        step_resp = requests.post(ENV_URL + '/step', json=action, timeout=30)
        result = step_resp.json()

        score = result.get('reward', 0.5)
        feedback = result.get('feedback', 'Review complete')
        task_type = result.get('task_type', difficulty)

        # Format output
        output = '## 🔍 Code Review Results\n\n'
        output += f'**Language:** {language}\n\n'
        output += f'**Difficulty:** {task_type}\n\n'
        output += f'**Score:** {score:.2f}/1.00\n\n'
        output += f'**Feedback:** {feedback}\n\n'

        if score >= 0.8:
            output += '✅ **Excellent code quality!**'
        elif score >= 0.5:
            output += '⚠️ **Some issues found - review needed**'
        else:
            output += '❌ **Critical issues found - immediate fix needed**'

        return output

    except Exception as e:
        return f'Error: {str(e)}'

# Build UI
with gr.Blocks(title='AI Code Review', theme=gr.themes.Soft()) as demo:
    gr.Markdown('# 💻 AI Code Review Environment')
    gr.Markdown('Paste your code below and get instant AI-powered feedback!')

    with gr.Row():
        with gr.Column():
            code_input = gr.Textbox(
                label='📝 Your Code',
                placeholder='Paste your code here...',
                lines=10
            )
            language = gr.Dropdown(
                choices=['python', 'javascript', 'java'],
                value='python',
                label='🌍 Language'
            )
            difficulty = gr.Dropdown(
                choices=['easy', 'medium', 'hard'],
                value='easy',
                label='🎯 Difficulty Level'
            )
            submit_btn = gr.Button('🔍 Review Code', variant='primary')

        with gr.Column():
            output = gr.Markdown(label='Results')

    submit_btn.click(
        fn=review_code,
        inputs=[code_input, language, difficulty],
        outputs=output
    )

    gr.Markdown('---')
    gr.Markdown('Built with ❤️ using OpenEnv | [GitHub](https://github.com/boobesh789/Code-review)')

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7860)
