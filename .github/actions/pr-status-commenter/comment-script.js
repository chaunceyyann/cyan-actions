const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const requiredChecks = process.env.INPUT_REQUIRED_CHECKS.split(',').map(c => c.trim());
    const successTemplate = process.env.INPUT_SUCCESS_TEMPLATE;
    const octokit = github.getOctokit(process.env.GITHUB_TOKEN);
    const context = github.context;

    // Get PR number
    const prNumber = context.payload.pull_request?.number;
    if (!prNumber) {
      console.log('No PR number found, skipping');
      return;
    }

    console.log(`Processing PR #${prNumber}`);

    // Get check runs for the latest commit
    const latestSha = context.payload.pull_request.head.sha;
    const { data: checkRuns } = await octokit.rest.checks.listForRef({
      owner: context.repo.owner,
      repo: context.repo.repo,
      ref: latestSha
    });

    // Find relevant checks (simple name matching)
    const relevantChecks = checkRuns.check_runs.filter(check =>
      requiredChecks.some(required => check.name.includes(required))
    );

    console.log(`Found ${relevantChecks.length} relevant checks`);

    // Check if all are completed and successful
    const allCompleted = relevantChecks.every(check => check.status === 'completed');
    const allSuccessful = relevantChecks.every(check => check.conclusion === 'success');

    if (!allCompleted) {
      console.log('Not all checks completed yet');
      return;
    }

    if (!allSuccessful) {
      console.log('Not all checks successful, skipping comment');
      return;
    }

    // Post success message using template
    const checksList = relevantChecks.map(check => `- ✅ ${check.name}`).join('\n');

    const commentBody = successTemplate
      .replace(/\{\{checks\}\}/g, checksList)
      .replace(/\{\{pr_number\}\}/g, prNumber)
      .replace(/\{\{repo\}\}/g, `${context.repo.owner}/${context.repo.repo}`);

    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: commentBody
    });

    console.log(`Posted success comment on PR #${prNumber}`);

  } catch (error) {
    console.error('Error:', error.message);
    core.setFailed(error.message);
  }
}

run();
