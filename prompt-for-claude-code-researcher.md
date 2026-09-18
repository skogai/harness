<request>

i want to create a environment for the claude code harness which essentially is as empty as possible and i would like you to help me find the relevant claude code settings, rules and recommendations. this will probably include things like creating a separate and new `global .claude/` folder. empty the system instructions, starting prompts and similar settings as well as de-activating all tooling, helpers and/or things which can be seen as opt-in features. the reasoning behind this is so we can create more focused and effective configurations and setup where everything which normally could help become a burden instead.

example: we have 50 rows of git diff which we need help to create a good descriptive commit message for. we have either the recommended way of doing things via claude-code-defaults or by starting with a claude which literally is takes `input` and returns `response`

1. the default claude-code-cli recommendations start with 35-45.000 tokens in context.
2. a minimil claude-code-cli start with 3000 tokens it context.

# 1 here we are forced to aggressively add a 1500 tokens explaining in detail that extra explanations, prose, verbose reasoning and "claude-code-things" do not belong in a 20 token commit for a 100 token diff.
# 2 here we have to add and redirect the input and output ourselves - normally done via redirecting simple pipes and appending to context-files.

</request>
