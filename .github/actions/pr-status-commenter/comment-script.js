const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const requiredChecks = process.env.INPUT_REQUIRED_CHECKS.split(',').map(c => c.trim());
    const successTemplate = process.env.INPUT_SUCCESS_TEMPLATE;
    const octokit = github.getOctokit(process.env.GITHUB_TOKEN);
    const context = github.context;

    const prNumber = context.payload.pull_request?.number;
    if (!prNumber) return;

    const { data: checkRuns } = await octokit.rest.checks.listForRef({
      owner: context.repo.owner,
      repo: context.repo.repo,
      ref: context.payload.pull_request.head.sha
    });

    const relevantChecks = checkRuns.check_runs.filter(check =>
      requiredChecks.some(required => check.name.includes(required))
    );

    const allCompleted = relevantChecks.every(check => check.status === 'completed');
    const allSuccessful = relevantChecks.every(check => check.conclusion === 'success');

    if (!allCompleted || !allSuccessful) return;

    // Get unique workflow names and sort alphabetically
    const workflowNames = [...new Set(relevantChecks.map(check => check.name.split('/')[0]))].sort();
    const checksList = workflowNames.join(' ✅ ');
    const commentBody = successTemplate.replace(/\{\{checks\}\}/g, checksList + ' ✅');

    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: commentBody
    });

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
