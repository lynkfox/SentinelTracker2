#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from stacks.tracker import Tracker


app = cdk.App()
Tracker(app, "SentinelsTracker")

app.synth()
