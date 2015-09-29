#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Jari Torniainen <jari.torniainen@ttl.fi>
# Finnish Institute of Occupational Health
# Copyright 2015
#
# This code is released under the MIT license
# http://opensource.org/licenses/mit-license.php
#
# Please see the file LICENSE for details


import pygame
import requests
import time


def request_hr():
    # TODO: Some kind of try-catch?
    address = 'http://127.0.0.1:8080/'
    request = 'ecgnode/metric/{"type":"mean_hr", "channels":["ch0"] , "time_window":[5], "arguments":[100]}'
    return round(requests.get(address + request).json()[0]['return'])


def request_rmssd():
    # TODO: Some kind of try-catch?
    address = 'http://127.0.0.1:8080/'
    request = 'ecgnode/metric/{"type":"rmssd", "channels":["ch0"] , "time_window":[15], "arguments":[100]}'
    return round(requests.get(address + request).json()[0]['return'])


def calculate_transition(current_value, target, increment):
    if current_value < target:
        current_value += increment
    elif current_value > target:
        current_value -= increment

    if abs(current_value - target) < increment:
        current_value = target

    return current_value


def main():
    width = 300
    height = 300
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    BACKGROUND_COLOR = (255, 255, 255)

    last_update = time.time()
    update_interval = 1
    font = pygame.font.SysFont('ProggySquareTT for Powerline', 50)

    target_hr = request_hr()
    current_hr = target_hr

    target_rmssd = request_rmssd()
    current_rmssd = target_rmssd

    text_hr = font.render('HR: {}'.format(current_hr), 1, (0, 0, 0))
    text_rmssd = font.render('RMSSD: {}'.format(current_rmssd), 1, (0, 0, 0))

    increment_hr = 0.1
    increment_rmssd = 0.1

    running = True
    while running:

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        if time.time() - last_update > update_interval:
            target_hr = request_hr()
            target_rmssd = request_rmssd()
            last_update = time.time()

        current_hr = calculate_transition(current_hr, target_hr, increment_hr)
        current_rmssd = calculate_transition(current_rmssd, target_rmssd, increment_rmssd)

        text_hr = font.render('HR:'.ljust(7) + '{}'.format(current_hr), 1, (0, 0, 0))
        text_rmssd = font.render('RMSSD:'.ljust(7) +  '{}'.format(current_rmssd), 1, (0, 0, 0))

        screen.fill(BACKGROUND_COLOR)
        screen.blit(text_hr, (10, 10))
        screen.blit(text_rmssd, (10, 50))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
