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

    // Remove all previous comments from this action
    await removePreviousComments(octokit, context, prNumber, successTemplate);

    // Create new comment
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

async function removePreviousComments(octokit, context, prNumber, successTemplate) {
  try {
    // Get all comments on the PR
    const { data: comments } = await octokit.rest.issues.listComments({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber
    });

    // Find comments that match our template pattern
    const commentsToDelete = comments.filter(comment => {
      // Check if comment contains the template pattern (without the checks part)
      const templateWithoutChecks = successTemplate.replace(/\{\{checks\}\}/g, '');
      return comment.body.includes(templateWithoutChecks) &&
             comment.user.type === 'Bot' &&
             comment.user.login.includes('github-actions');
    });

    // Delete all matching comments
    for (const comment of commentsToDelete) {
      await octokit.rest.issues.deleteComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        comment_id: comment.id
      });
    }

    if (commentsToDelete.length > 0) {
      console.log(`Removed ${commentsToDelete.length} previous comment(s)`);
    }
  } catch (error) {
    console.warn('Failed to remove previous comments:', error.message);
    // Don't fail the action if comment removal fails
  }
}

run();
