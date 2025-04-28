import os
import json
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ReactGenerator:
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.groq_client = Groq(api_key=api_key)
    
    def generate_react_project(self, requirements: str, project_path: Path) -> dict:
        """
        Generate a complete React project with actual files
        """
        # Create basic project structure
        project_path.mkdir(exist_ok=True)
        src_path = project_path / "src"
        src_path.mkdir(exist_ok=True)
        
        # Generate package.json with stable dependencies
        package_json = {
            "name": project_path.name,
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^17.0.2",
                "react-dom": "^17.0.2",
                "react-router-dom": "^5.3.4",
                "styled-components": "^5.3.6"
            },
            "devDependencies": {
                "@babel/core": "^7.18.10",
                "@babel/preset-react": "^7.18.6",
                "babel-loader": "^8.2.5",
                "webpack": "^5.74.0",
                "webpack-cli": "^4.10.0",
                "webpack-dev-server": "^4.11.1",
                "html-webpack-plugin": "^5.5.1",
                "css-loader": "^6.7.1",
                "style-loader": "^3.3.1"
            },
            "scripts": {
                "start": "webpack serve --mode development --open",
                "build": "webpack --mode production"
            }
        }
        
        with open(project_path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Generate webpack.config.js
        webpack_config = """const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html'
    })
  ],
  resolve: {
    extensions: ['.js', '.jsx']
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    compress: true,
    port: 3000,
  }
};"""
        
        with open(project_path / "webpack.config.js", "w") as f:
            f.write(webpack_config)
        
        # Generate .babelrc
        babelrc = """{
  "presets": ["@babel/preset-react"]
}"""
        
        with open(project_path / ".babelrc", "w") as f:
            f.write(babelrc)
        
        # Generate main App component
        app_js = self.generate_component("App", requirements)
        with open(src_path / "App.js", "w") as f:
            f.write(app_js)
        
        # Generate index.js
        index_js = """import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);"""
        
        with open(src_path / "index.js", "w") as f:
            f.write(index_js)
        
        # Generate basic CSS
        index_css = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}"""
        
        with open(src_path / "index.css", "w") as f:
            f.write(index_css)
        
        # Generate public/index.html
        public_path = project_path / "public"
        public_path.mkdir(exist_ok=True)
        
        index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>"""
        
        with open(public_path / "index.html", "w") as f:
            f.write(index_html)
        
        # Generate components based on requirements
        components = self.generate_components(requirements)
        components_path = src_path / "components"
        components_path.mkdir(exist_ok=True)
        
        for component_name, component_code in components.items():
            with open(components_path / f"{component_name}.js", "w") as f:
                f.write(component_code)
        
        return {
            "message": "React project generated successfully",
            "project_path": str(project_path),
            "components": list(components.keys())
        }
    
    def generate_components(self, requirements: str) -> dict:
        """
        Generate multiple React components based on requirements
        """
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert React developer. Based on the requirements, generate multiple React components.
                    Return the response as a JSON object where keys are component names and values are the component code.
                    Each component should be a complete, functional React component with proper styling."""
                },
                {
                    "role": "user",
                    "content": f"Generate React components for: {requirements}"
                }
            ]
        )
        
        try:
            components = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Default components if parsing fails
            components = {
                "Header": """import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  background-color: #282c34;
  padding: 20px;
  color: white;
  text-align: center;
`;

const Header = () => {
  return (
    <HeaderContainer>
      <h1>React Application</h1>
    </HeaderContainer>
  );
};

export default Header;""",
                "Footer": """import React from 'react';
import styled from 'styled-components';

const FooterContainer = styled.footer`
  background-color: #282c34;
  padding: 20px;
  color: white;
  text-align: center;
  position: fixed;
  bottom: 0;
  width: 100%;
`;

const Footer = () => {
  return (
    <FooterContainer>
      <p>© 2024 React Application</p>
    </FooterContainer>
  );
};

export default Footer;"""
            }
        
        return components
    
    def generate_component(self, component_name: str, requirements: str) -> str:
        """
        Generate a React component based on requirements
        """
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert React developer. Generate a complete React component with proper styling and functionality."
                },
                {
                    "role": "user",
                    "content": f"Generate a React component named {component_name} with these requirements: {requirements}"
                }
            ]
        )
        
        return response.choices[0].message.content
    
    def generate_page(self, page_name: str, requirements: str) -> str:
        """
        Generate a React page component based on requirements
        """
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert React developer. Generate a complete React page component with routing and proper styling."
                },
                {
                    "role": "user",
                    "content": f"Generate a React page component named {page_name} with these requirements: {requirements}"
                }
            ]
        )
        
        return response.choices[0].message.content 