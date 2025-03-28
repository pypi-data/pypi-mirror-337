# Changelog

## [Version 0.4.5] - 2025-03-27

### Fix

- Removed redundancies and moved mutable class attributes into the __init__ method

## [Version 0.4.4] - 2024-11-19

### Fix

- Forgot to add dots to the end of each post split when post length is less than the post limit but it will be more than the limit after the provided tag(s) is/are added to it, this bug was originally fixed in v0.4.1 but forgot to add dots to the splitted post, and this has been fixed.

## [Version 0.4.3] - 2024-11-19

### Fix

- Forgot to uncomment some lines of code I commented out when testing.

## [Version 0.4.2] - 2024-11-19

### Fix

- Perfected the bug fix in version 0.4.1 because the update caused rest of the part of the post text to be stripped off and replaced with the tag, now fixed and working properly.

## [Version 0.4.1] - 2024-11-19

### Fix

- Fixed a bug in the `__split_post__` method in which post length that is a bit less than 500 will get returned with the added tag making it go above the post limit.

## [Version 0.4.0] - 2024-11-12

### Added

- Added the update to the Meta's Threads API released on October 28, 2024, the `shares` metric indicating the number of shares of a Threads post

### Fix

- Fixed a bug in the `get_auth_token` method in which the `scope` property was not handled to handle the case where user provided a single scope.

## [Version 0.3.0] - 2024-10-14

### Added

- Added the update to the Meta's Threads API released on October 9, 2024 for the support for post quoting and reposts to ThreadsPipe.

### Fix

- In the `__refresh_token__` function in the cli.py file I changed the return statement in the status code check to `pprint.pp`.

## [Version 0.2.1] - 2024-09-27

### Fix

- A bug caused by method that checks if a file is base64 or not and causes error if the file is a binary

## [Version 0.2.0] - 2024-09-20

### Fix

- I added the method that I forgot to add that will delete the temporarily uploaded github files when the post debug check before publishing posts fails.

### Added

- Added the recent update (released on September 19, 2024) to the Meta's Threads API for the increase number of media files that can be in a post and updated the limit in the README.

## [Version 0.1.6] - 2024-09-18

### Fix

- Fixed a bug in pipe method in which the tags at the end posts that has newline or space characters are ignored

### Added

- Added `link_attachment_url` to the list of items to be returned for `get_post` abd `get_posts`.
- Added `threads_api_version` parameter, for changing/setting the Threads API version number, to the class object parameter and to the `update_param` method.

## [Version 0.1.5] - 2024-09-17

### Fix

- Fixed a bug in the `__split_post__` method causing the next batch of splitted posts, after adding hashtags, to reset back to the beginning.

## [Version 0.1.4] - 2024-09-17

### Added
  
- A test case for the supported file url formats
- Support for ip address file urls added
- Added support for ports in file urls

### Fix

- A fix for the RegExp check for file urls, the former RegExp doesn't pass for some urls and only matches some url formats and that caused errors which results into treating some file urls as local files.

## [Version 0.1.3] - 2024-09-17

### Fix

- A bug fix in the pipe method.

## [Version 0.1.2] - 2024-09-16

### Fix

- A bug fix in the pipe method.

## [Version 0.1.1] - 2024-09-16

### Fix

- A bug in the send_post method

## [Version 0.1.0] - 2024-09-16

### Added

- Added the `link_attachment` parameter to the `pipe` method for explicitly adding links to text-only posts
- Added response object to the ThreadsPipe response method `__tp_response_msg__`
