# Environment Profile Switching

## Summary
Implement a feature to create, manage, and switch between multiple environment profiles (dev, test, prod, etc.) in the settings editor.

## Description
This task focuses on adding the ability to create and switch between different environment configurations (.env files) for different contexts (development, testing, production, etc.). The currently active profile will be the main .env file, while other profiles will be stored as separate files with naming convention .env_[profile_name].

## User Story
[US001 - Environment Settings Editor](../userstories/done/US001-Settings-Editor.md)

## Technical Requirements
- Create a mechanism to detect and list available environment profiles
- Implement functionality to switch between profiles (copying the selected profile to .env)
- Add ability to create new profiles based on existing ones
- Store the profile name as a comment in the first row of each env file
- Ensure profile switching preserves all settings and comments
- Implement backup functionality before switching profiles
- Add UI components for profile management
- Handle confirmation for profile switching to prevent accidental changes

## Implementation Plan
1. Create a function to detect and list available environment profiles
2. Implement profile switching functionality (with proper backups)
3. Add profile creation functionality
4. Add profile deletion/renaming capability
5. Update the settings editor main menu to include profile management
6. Add UI components for profile selection, creation, and management
7. Implement status indicators for the current active profile
8. Add confirmation dialogs for profile switching

## Definition of Done
- Users can view a list of available environment profiles
- Users can switch between profiles with proper confirmation
- Users can create new profiles based on existing ones
- Users can rename or delete existing profiles
- The current active profile is clearly indicated in the UI
- Profile switching is safe and preserves all settings
- Profiles are stored with proper naming conventions (.env, .env_dev, .env_prod, etc.)
- Profile names are stored as comments in the first row of each env file

## Dependencies
- Task 001 (Settings Editor Implementation)
- Task 003 (Environment File Operations)
- Python's os, io, and shutil modules

## Related Tasks
- [001-env-settings-editor.md](../tasks/done/001-env-settings-editor.md)
- [003-env-settings-file-operations.md](../tasks/done/003-env-settings-file-operations.md)

## Estimated Effort
Medium - Approximately 3-4 hours of development time

## Priority
High - This is an essential feature for workflow efficiency

## Assignee
TBD

## Status
Completed - May 21, 2024

## Implementation Notes
- Implemented get_current_profile() function to detect the active profile
- Created get_available_profiles() function to find all profile files
- Implemented manage_profiles() function as the main profile management interface
- Added switch_profile() function to safely change between profiles
- Implemented create_profile() to make new profiles from existing ones or templates
- Added rename_profile() and delete_profile() functions with proper validation
- Created a dedicated UI section for profile management
- Added clear visual indicators for the active profile
- Implemented confirmation dialogs for all potentially destructive operations
- Ensured proper backup before profile switching operations 