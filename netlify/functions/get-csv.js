// netlify/functions/get-csv.js

exports.handler = async function(event, context) {
    // Get the GitHub token from the secure environment variables
    const GITHUB_TOKEN = process.env.GITHUB_PAT;

    // The API URL for the raw content of your private file
    const GITHUB_API_URL = 'https://api.github.com/repos/Bosch-Rexroth-OCS/agent-check/contents/result.csv';

    try {
        const response = await fetch(GITHUB_API_URL, {
            method: 'GET',
            headers: {
                // Authenticate with your Personal Access Token
                'Authorization': `token ${GITHUB_TOKEN}`,
                // The GitHub API requires this header to get the raw file content
                'Accept': 'application/vnd.github.v3.raw',
            }
        });

        if (!response.ok) {
            // If the response is not successful, throw an error
            throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
        }

        // Get the CSV text from the response
        const csvData = await response.text();

        // Return the CSV data to the front-end
        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'text/csv',
            },
            body: csvData,
        };

    } catch (error) {
        console.error('Error fetching from GitHub:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Failed to fetch data from private repository.' }),
        };
    }
};