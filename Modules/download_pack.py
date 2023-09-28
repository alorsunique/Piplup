# Package with the necessary functions for downloads

import random
import sys
import time

from instaloader import Profile  # Import Instaloader

up_new_dl = 200  # Upper limit for new downloads before a short download break
up_done_dl = 1000


def short_pause():  # Pause in seconds
    min_time_bound = 5
    max_time_bound = 15
    time_sleep = int(random.randint(min_time_bound, max_time_bound))
    print(f"Waiting for {time_sleep} seconds")
    time.sleep(time_sleep)
    # Time is returned to keep track of total wait time
    return time_sleep


def long_pause():  # Pause in minutes
    min_time_bound = 5
    max_time_bound = 10
    time_sleep = int(random.randint(min_time_bound, max_time_bound))
    print(f"Waiting for {time_sleep} minutes.")
    time.sleep(time_sleep)
    # Time is returned to keep track of total wait time
    return time_sleep * 60


# Post compare download will download everything until the max download is achieved
# A skip option can be added to skip N amount of files that are downloaded
# Not skipping the files can also be done to verify if everything under that post got downloaded
def post_compare_download(L_instance, account, offline_list, max_dl, net_counter, max_pass):
    profile = Profile.from_username(L_instance.context, account)  # Retrieve profile of account

    L_instance.save_profile_id(profile)  # Download the profile ID
    L_instance.download_profile(profile, profile_pic=True, profile_pic_only=True)  # Download the profile picture

    # Condition for the pass of already downloaded files
    pass_count = 0
    pass_condition = False

    # Counters
    new_dl_count = 0
    done_dl_count = 0
    wait_time = 0
    check_new_dl_count = 1
    check_done_dl_count = 1

    for post in profile.get_posts():

        print(f"Post: {post}")

        # This allows downloading of new post before hitting the pass condition. This is because more recent posts
        # are not going to be on the offline list and will be skipped without this segment.
        if post not in offline_list and not pass_condition:
            L_instance.download_post(post, account)

            new_dl_count += 1
            net_counter[0] += 1
            print(f"New Download. Download from account: {new_dl_count} | Download from session: {net_counter[0]}")

            if check_new_dl_count < up_new_dl:
                check_new_dl_count += 1
                time_sleep = short_pause()
                wait_time += time_sleep
                net_counter[1] += time_sleep
            else:
                check_new_dl_count = 1
                time_sleep = long_pause()
                wait_time += time_sleep
                net_counter[1] += time_sleep

        else:
            pass_count += 1
            print(f"Pass count: {pass_count}")

            if pass_count > max_pass:
                pass_condition = True

        # If pass condition is true, max skip has been done. All following posts from get posts will
        # be checked by the download post. This is the old run through code
        if pass_condition:
            check = L_instance.download_post(post, account)  # Boolean check if post is downloaded

            if check:  # True if not downloaded. Proceeds to download
                new_dl_count += 1
                net_counter[0] += 1
                print(f"New Download. Download from account: {new_dl_count} | Download from session: {net_counter[0]}")

                if check_new_dl_count < up_new_dl:
                    check_new_dl_count += 1
                    time_sleep = short_pause()
                    wait_time += time_sleep
                    net_counter[1] += time_sleep
                else:
                    check_new_dl_count = 1
                    time_sleep = long_pause()
                    wait_time += time_sleep
                    net_counter[1] += time_sleep

            else:  # False if already downloaded. Here post is already downloaded so it is skipped
                done_dl_count += 1
                print(f"Post Already Downloaded. Run through downloaded posts: {done_dl_count}")

                if check_done_dl_count < up_done_dl:
                    time_sleep = int(random.randint(2, 5))
                    print(f"Wait for {time_sleep} seconds")
                    check_done_dl_count += 1
                    wait_time += time_sleep
                    net_counter[1] += time_sleep
                    time.sleep(time_sleep)
                else:
                    time_sleep = int(random.randint(2, 3))
                    print(f"Wait for {time_sleep} minute")
                    check_done_dl_count = 1
                    wait_time += 60 * time_sleep
                    net_counter[1] += 60 * time_sleep
                    time.sleep(60 * time_sleep)

        # Code only finishes after downloading the desired amount or all posts are exhausted
        if new_dl_count >= max_dl:
            break

    return net_counter, new_dl_count, wait_time


# Post compare update is used to update profiles. It can be used for almost all purposes except
# when verifying that all files under a post have been downloaded
def post_compare_update(L_instance, account, offline_list, max_dl, net_counter, max_dl_skip):
    profile = Profile.from_username(L_instance.context, account)

    L_instance.save_profile_id(profile)
    L_instance.download_profile(profile, profile_pic=True, profile_pic_only=True)

    new_dl_count = 0
    done_dl_count = 0

    wait_time = 0
    check_new_dl_count = 1

    for post in profile.get_posts():
        if post not in offline_list:
            sys.stdout.write(f"\r\n")
            print(f"Post: {post}")
            L_instance.download_post(post, account)

            new_dl_count += 1
            net_counter[0] += 1
            print(f"New Download. Download from account: {new_dl_count} | Download from session: {net_counter[0]}")

            if check_new_dl_count < up_new_dl:
                check_new_dl_count += 1
                time_sleep = short_pause()
                wait_time += time_sleep
                net_counter[1] += time_sleep
            else:
                check_new_dl_count = 1
                time_sleep = long_pause()
                wait_time += time_sleep
                net_counter[1] += time_sleep

        else:
            done_dl_count += 1
            sys.stdout.write(f"\rPost already downloaded: Skipped {done_dl_count}")

        if new_dl_count >= max_dl or done_dl_count >= max_dl_skip:
            break

    return net_counter, new_dl_count, wait_time
