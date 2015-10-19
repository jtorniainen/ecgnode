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
    request = 'ecgnode/metric/{"type":"rmssd", "channels":["ch0"] , "time_window":[30], "arguments":[100]}'
    return round(requests.get(address + request).json()[0]['return'])


def calculate_transition(current_value, target, increment):
    if current_value < target:
        current_value += increment
    elif current_value > target:
        current_value -= increment

    if abs(current_value - target) < increment:
        current_value = target

    return current_value


def render_text(font, string, value, color=(0, 0, 0)):
    return font.render(string.ljust(7) + '{}'.format(value), 1, color)


def main():
    width = 600
    height = 200
    pygame.init()
    pygame.display.set_caption('HRV-monitor')
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    BACKGROUND_COLOR = (0, 0, 0)
    TEXT_COLOR = (255, 255, 255)

    last_update = time.time()
    update_interval = 1
    font = pygame.font.SysFont('Monospace', 70)

    target_hr = request_hr()
    current_hr = target_hr

    target_rmssd = request_rmssd()
    current_rmssd = target_rmssd

    text_hr = render_text(font, 'HR:', current_hr)
    text_rmssd = render_text(font, 'RMSSD:', current_rmssd)

    increment_hr = 1.0
    increment_rmssd = 1.0

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

        #current_hr = calculate_transition(current_hr, target_hr, increment_hr)
        #current_rmssd = calculate_transition(current_rmssd, target_rmssd, increment_rmssd)
        current_hr = target_hr
        current_rmssd = target_rmssd

        text_hr = render_text(font, 'HR:', current_hr, TEXT_COLOR)
        text_rmssd = render_text(font, 'RMSSD:', current_rmssd, TEXT_COLOR)

        screen.fill(BACKGROUND_COLOR)
        screen.blit(text_hr, (10, 10))
        screen.blit(text_rmssd, (10, 100))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
