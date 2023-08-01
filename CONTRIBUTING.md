# CONTRIBUTING GUIDELINES

### Branch Naming

To have a consitent and well-defined branch naming convention for effective collaboration and verson control management, please following the following guidelines

#### 1. Branch Prefixes:

Consider using specific prefixes to indicate the purpose of the branch. For example:

- `feature/` for new feature development
- `bugfix/` for bug fixes
- `hotfix/` for critical bug fixes
- `release/` for release preparation
- `docs/` for documentation updates
- `chore/` for maintenance or other non-feature tasks

For example, if you are working on a new feature for addind users, you might create a branch with the name `feature/add-user`. If it's a bugfix, you might use `bugfix/fix-validation-bug`.

#### 2. Use Hyphens

Use hyphens to separate words in the branch name for better readability. For example, `feature/add-user` or `bugfix/fix-validation-bug`.

#### 3. Short and Meaningful

Keep branch names concise but meaningful. Avoid excessively long names that may become cumbersome.

#### 4. Lowercase Letters

Use lowercase letters for branch names to maintain consistency and avoid potential issues with case sensitivity on different operating systems.

#### 5. Avoid Special Characters

Avoid using special characters or spaces in branch names to ensure compatibility across various version control systems.

#### 6. Use Descriptive Names

Choose branch names that clearly describe the purpose or the feature being worked on. Avoid generic names like "branch1" or "fix_bug".

### Use Meaningful commit messages

#### 1. Be Descriptive

Start the commit message with a concise description of what the commit accomplishes. Use the imperative mood (`Add`, `Fix`, `Update`, `Refactor`, `Revert`, `test`, `chore`) to indicate the action performed.

#### 2. Reference Issues

If the commit relates to an issue or task, include a reference to it using issue numbers (e.g., "Fixes #123," "Closes #456,").

#### 3. Be Consistent:

Use the same commit style throughout to keep consistency
forexample
```shell
 docs: correct spelling of CHANGELOG
```

Reference

[Converntional Commites](https://www.conventionalcommits.org/en/v1.0.0/)
