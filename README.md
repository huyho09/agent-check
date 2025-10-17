# Agent-Check

This project is a tool for monitoring and reporting the availability of agents from an API endpoint. It includes a Python script for collecting data and a web-based dashboard for visualizing the results.

## Purpose of the Project

The primary purpose of this project is to track the availability of chat agents for the **GP\_Bosch\_Rexroth\_Chat\_DC\_VAG** service. It periodically checks an API endpoint, records the number of available agents, and stores this data in a CSV file. A web interface is provided to visualize this data, allowing users to filter by date and availability status. This helps in monitoring service uptime and agent availability over time.

-----

## Project Setup

The project is divided into two main parts: a **backend** Python script for data collection and a **frontend** web dashboard for data visualization.

### Backend Setup (Python)

The backend consists of a Python script (`main.py`) that fetches the agent availability data.

1.  **Prerequisites**:

      * Python 3.x installed.

2.  **Installation**:

      * Clone the repository to your local machine.
      * Navigate to the project directory.
      * Install the required Python packages using pip:
        ```bash
        pip install -r requirements.txt
        ```

### Frontend Setup (Web Dashboard)

The frontend is a static web page that displays the collected data. It is designed to be deployed on **Netlify** and uses a serverless function to fetch the data from a GitHub repository.

1.  **Prerequisites**:

      * Node.js and npm installed.

2.  **Installation**:

      * Run the following command in the project root to install the necessary npm packages:
        ```bash
        npm install
        ```

3.  **Configuration**:

      * The web dashboard uses a Netlify function (`netlify/functions/get-csv.js`) to fetch the `result.csv` file from a private GitHub repository.
      * To make this work, you need to create a **GitHub Personal Access Token (PAT)** with at least `repo` scope (for private repositories).
      * When deploying to Netlify, you must set an environment variable named `GITHUB_PAT` with the value of your GitHub token.

-----

## How to Run the Project

### Running the Backend

The Python script (`main.py`) is designed to be run periodically to collect data. You can run it manually or set up a scheduled task.

  * **Manual Execution**:

    ```bash
    python main.py
    ```

    This will run the script once, check the API, and append the result to `result.csv`.

  * **Scheduled Execution (Automation)**:
    For continuous monitoring, it is recommended to run the script on a schedule. You can use:

      * **Cronjob** on a Linux server.
      * **Scheduled Tasks** on a Windows server.
      * **GitHub Actions** with a scheduled trigger (as suggested in the script's comments) to run the script at regular intervals (e.g., every 15 minutes).

### Running the Frontend

The frontend is a static website that can be viewed in a few ways:

  * **Local Development**:
    You can use a simple local web server to view the `index.html` file. However, the data fetching from the Netlify function will not work locally without additional setup (like using the Netlify CLI).

  * **Deployment**:
    The intended way to use the frontend is to deploy the project to **Netlify**.

    1.  Push your project to a GitHub repository.
    2.  Create a new site on Netlify and link it to your GitHub repository.
    3.  Set up the `GITHUB_PAT` environment variable in the Netlify site settings.
    4.  Deploy the site. Netlify will automatically build and deploy the site and the serverless function.

-----

## Business Use Cases and Benefits

This project provides valuable insights into agent availability, which can be leveraged for various business purposes:

  * **📈 Service Level Agreement (SLA) Monitoring**: Track agent availability to ensure that you are meeting your SLA commitments to customers. This data can be used to generate reports and provide evidence of compliance.

  * **👥 Resource and Staffing Optimization**: By analyzing the historical data, you can identify peak hours and days for customer inquiries. This allows for better scheduling of agents to meet demand, reducing customer wait times and improving satisfaction.

  * **⚠️ Proactive Issue Detection**: A sudden drop in available agents to zero or a "Connection Error" can be an early indicator of a service outage or technical issue. This allows your IT team to be alerted and respond to problems before they significantly impact customers.

  * **📊 Performance and Trend Analysis**: The dashboard can help you visualize trends in agent availability over weeks or months. This can help in understanding the impact of marketing campaigns, new product launches, or seasonal demand on your support team.

  * \*\* Forecasting and Capacity Planning\*\*: Historical data on agent availability can be used to forecast future demand. This is essential for capacity planning, helping you decide when to hire and train new agents to handle anticipated growth.

  * **✅ Auditing and Reporting**: The collected data provides a historical log of agent availability, which can be used for internal audits, performance reviews, and generating reports for management on the efficiency and reliability of the customer support service.