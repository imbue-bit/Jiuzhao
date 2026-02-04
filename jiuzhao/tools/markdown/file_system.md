Name: file_system
Description: Read and write files in the local project directory.
Usage:
<TOOL name="file_system">
{
  "action": "write", 
  "path": "filename.lean", 
  "content": "..."
}
</TOOL>
or
<TOOL name="file_system">
{
  "action": "read", 
  "path": "filename.lean"
}
</TOOL>
