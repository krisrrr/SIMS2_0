#!/usr/bin/env python3
import time
from datetime import datetime
from bluepy.btle import BTLEDisconnectError
from .models import *
from .miband import miband
from .classes.activity import ActivityEntity

colors = {
    0: 'grey',
    1: 'lightskyblue',
    2: 'royalblue'
}


def write_to_db(activity):
    with open("activity/current_user.txt", "r") as f:
        user = f.read().strip()
    entry = Activity(
        date_time=activity.timestamp,
        category_num=activity.category,
        intensity=activity.intensity,
        steps=activity.steps,
        heart_rate=activity.heart_rate,
        user=user
    )
    entry.save()


def activities_callback(activity: ActivityEntity):
    write_to_db(activity)


def try_to_connect(mac_address, auth_key):
    success = False
    for i in range(10):
        try:
            band = miband(mac_address, auth_key, debug=True)
            success = band.initialize()
            return band
        except BTLEDisconnectError:
            print('Connection to the MIBand failed. Trying out again in 3 seconds')
            time.sleep(3)
            continue
    return False


def get_activity_logs(start, mac_address, auth_key):
    band = try_to_connect(mac_address, bytes.fromhex(auth_key))
    if not band:
        return False
    band.get_activity_betwn_intervals(start, datetime.now(), activities_callback)
    for i in range(20):
        band.waitForNotifications(0.2)
        if Activity.objects.exists():
            last_datetime = Activity.objects.order_by('-id')[0].date_time
            now = datetime.now()
            if (
                    last_datetime.day == now.day and
                    last_datetime.month == now.month and
                    last_datetime.year == now.year and
                    last_datetime.hour == now.hour and
                    last_datetime.minute == now.minute
            ):
                break
            if Activity.objects.filter(
                    date_time=datetime.fromtimestamp(now.timestamp() - 60 * 60
                                                     ).strftime("%Y-%m-%d %H:%M:%S")
            ) is None:
                return 0
            else:
                return 1


def sleeping(user):
    print('from sleeping func')
    now = datetime.now()
    end = datetime.fromtimestamp(now.timestamp() - 60 * 10)
    r = datetime.fromtimestamp(now.timestamp() - 4 * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
    begining = datetime.strptime(r[:-8] + '20:00:00', "%Y-%m-%d %H:%M:%S")
    datetime_of_current_iter = begining
    while True:
        current_entry = Activity.objects.filter(
            date_time=datetime_of_current_iter,
            user=user
        )
        ten_entries = [current_entry, ]
        for i in range(9):
            datetime_local = datetime.fromtimestamp(datetime_of_current_iter.timestamp() + 60 * (i + 1))
            ten_entries.append(Activity.objects.filter(
                date_time=datetime_local.strftime("%Y-%m-%d %H:%M:%S"),
                user=user
            ))

        steps = True
        for i in range(len(ten_entries)):
            try:
                if ten_entries[i][0].steps != 0:
                    steps = False
            except IndexError:
                break
        is_sleeping = 0
        sleep_phase = 0
        if steps:
            average = 0
            for i in range(len(ten_entries)):
                try:
                    if ten_entries[i][0].steps != 0:
                        average += ten_entries[i][0].intensity
                except IndexError:
                    break
            average = average / len(ten_entries)

            count_of_zero_intensity = 0
            for i in range(len(ten_entries)):
                try:
                    if ten_entries[i][0].intensity == 0:
                        count_of_zero_intensity += 1
                except IndexError:
                    break

            if count_of_zero_intensity > 5:
                intensity = True
            else:
                intensity = False
            try:
                if Activity.objects.filter(
                    date_time=datetime_of_current_iter.strftime("%Y-%m-%d %H:%M:%S"),
                    user=user
            )[0].heart_rate == 255:
                    pulse_255 = True
                else:
                    pulse_255 = False
            except IndexError:
                break

            pr_entry = Activity.objects.filter(
                date_time=datetime.fromtimestamp(
                    datetime_of_current_iter.timestamp() - 60).strftime("%Y-%m-%d %H:%M:%S"),
                user=user)[0]

            try:
                next_pulse = Activity.objects.filter(
                    date_time=datetime.fromtimestamp(
                        datetime_of_current_iter.timestamp() + 60).strftime("%Y-%m-%d %H:%M:%S"),
                    user=user)[0].heart_rate
            except IndexError:
                break

            pr_pr_entry = Activity.objects.filter(
                date_time=datetime.fromtimestamp(
                    datetime_of_current_iter.timestamp() - 120).strftime("%Y-%m-%d %H:%M:%S"),
                user=user)[0]

            pr_pr_pr_entry = Activity.objects.filter(
                date_time=datetime.fromtimestamp(
                    datetime_of_current_iter.timestamp() - 180).strftime("%Y-%m-%d %H:%M:%S"),
                user=user)[0]

            pr_pr_pr_pr_entry = Activity.objects.filter(
                date_time=datetime.fromtimestamp(
                    datetime_of_current_iter.timestamp() - 240).strftime("%Y-%m-%d %H:%M:%S"),
                user=user)[0]

            if pulse_255 or (pr_entry.heart_rate == 255 and next_pulse == 255):
                pulse = True
            else:
                pulse = False
            if average < 10 and intensity and pulse:
                is_sleeping = 1
                if pr_entry.is_sleeping == 0:
                    sleep_phase = 1
                if pr_entry.is_sleeping == 1:
                    count_of_809089_cats = 0
                    for i in range(len(ten_entries)):
                        try:
                            if 89 <= ten_entries[i][0].category_num <= 91 or ten_entries[i][0].category_num == 80:
                                count_of_809089_cats += 1
                        except IndexError:
                            break

                    change_phase = False
                    if pr_entry.sleep_phase == pr_pr_entry.sleep_phase and \
                            pr_entry.sleep_phase == pr_pr_pr_entry.sleep_phase and \
                            pr_pr_pr_pr_entry.sleep_phase == pr_entry.sleep_phase:
                        change_phase = True

                    vals = (80, 89, 90, 91)
                    if ten_entries[0][0].category_num in vals and count_of_809089_cats > 4 and change_phase:
                        # смена фазы
                        if pr_entry.sleep_phase == 1:
                            sleep_phase = 2
                        elif pr_entry.sleep_phase == 2:
                            sleep_phase = 1
                    else:
                        sleep_phase = pr_entry.sleep_phase
        Activity.objects.filter(
            date_time=datetime_of_current_iter.strftime("%Y-%m-%d %H:%M:%S"),
            user=user
        ).update(
            is_sleeping=is_sleeping,
            sleep_phase=sleep_phase
        )
        datetime_of_current_iter = datetime.fromtimestamp(
                    datetime_of_current_iter.timestamp() + 60)
        if datetime_of_current_iter == end:
            break


def get_entries_from_start(user):
    r = datetime.fromtimestamp(datetime.now().timestamp() - 5 * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
    start = datetime.strptime(r[:-8] + '20:00:00', "%Y-%m-%d %H:%M:%S")
    current_entry = Activity.objects.filter(
        date_time=start,
        user=user
    )
    entries = [current_entry, ]
    i = 1
    for i in range(960):
        datetime_local = datetime.fromtimestamp(start.timestamp() + 60 * i)
        entries.append(Activity.objects.filter(
            date_time=datetime_local.strftime("%Y-%m-%d %H:%M:%S"),
            user=user
        ))
    return entries


def sleep_graph(user):
    entries = get_entries_from_start(user)
    count_of_periods = []
    for i in range(959):
        if entries[i][0].sleep_phase != entries[i+1][0].sleep_phase:
            count_of_periods.append([])
            count_of_periods[-1].append(entries[i][0].sleep_phase)
    j = -1
    for i in range(len(count_of_periods)):
        count_of_periods[i].append(0)
        while True:
            j += 1
            if entries[j][0].sleep_phase == entries[j+1][0].sleep_phase:
                count_of_periods[i][1] += 1
            else:
                break

    return count_of_periods

