const core = require('@actions/core');
const { execSync } = require('child_process');

async function run() {
  try {
    const changedFiles = core.getInput('changed-files');
    const environment = core.getInput('environment');

    // Execute Python script
    const pythonScript = `
import os
import sys

# Account mappings
account_mappings = {
    'prod_account_number': {
        'src': 'prod_src_account',
        'tests': 'prod_tests_account',
        'default': 'prod_default_account'
    },
    'dev_account_number': {
        'src': 'dev_src_account',
        'tests': 'dev_tests_account',
        'default': 'dev_default_account'
    }
}

changed_files = '${changedFiles}'
environment = '${environment}'

# Determine account type
if '^src/' in changed_files:
    account_type = 'src'
elif '^tests/' in changed_files:
    account_type = 'tests'
else:
    account_type = 'default'

# Get account number
if environment in account_mappings:
    account_number = account_mappings[environment][account_type]
    print(account_number)
else:
    sys.exit(1)
`;

    const accountNumber = execSync(`python3 -c "${pythonScript}"`, { encoding: 'utf8' }).trim();
    core.setOutput('account_number', accountNumber);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run(); 