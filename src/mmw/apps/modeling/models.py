# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from django.contrib.gis.db import models
from django.contrib.auth.models import User

from apps.core.models import Job


class Project(models.Model):
    TR55 = 'tr-55'
    GWLFE = 'gwlfe'
    MODEL_PACKAGES = (
        (TR55, 'Site Storm Model'),
        (GWLFE, 'Watershed Multi-Year Model'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(
        max_length=255)
    area_of_interest = models.MultiPolygonField(
        null=True,
        help_text='Base geometry for all scenarios of project')
    area_of_interest_name = models.CharField(
        null=True,
        max_length=255,
        help_text='A human name for the area of interest')
    is_private = models.BooleanField(
        default=True)
    model_package = models.CharField(
        choices=MODEL_PACKAGES,
        max_length=255,
        help_text='Which model pack was chosen for this project')
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True)
    modified_at = models.DateTimeField(
        auto_now=True)
    is_activity = models.BooleanField(
        default=False,
        help_text='Projects with special properties')
    gis_data = models.TextField(
        null=True,
        help_text='Serialized JSON representation of additional'
                  ' data gathering steps, such as MapShed.')
    mapshed_job_uuid = models.ForeignKey(
        Job,
        to_field='uuid',
        related_name='mapshed_job',
        null=True,
        help_text='The job used to calculate the MapShed results.'
                  ' Used for getting the results of that job.')
    subbasin_mapshed_job_uuid = models.ForeignKey(
        Job,
        to_field='uuid',
        related_name='subbasin_mapshed_job',
        null=True,
        help_text='The job used to calculate the MapShed results'
                  ' for each HUC-12 sub-basin of the shape.')
    wkaoi = models.CharField(
        null=True,
        max_length=255,
        help_text='Well-Known Area of Interest ID for faster geoprocessing')

    def __unicode__(self):
        return self.name


class Scenario(models.Model):

    class Meta:
        unique_together = ('name', 'project')

    name = models.CharField(
        max_length=255)
    project = models.ForeignKey(Project, related_name='scenarios')
    is_current_conditions = models.BooleanField(
        default=False,
        help_text='A special type of scenario without modification abilities')
    inputs = models.TextField(
        null=True,
        help_text='Serialized JSON representation of scenario inputs')
    inputmod_hash = models.CharField(
        max_length=255,
        null=True,
        help_text='A hash of the values for inputs & modifications to ' +
                  'compare to the existing model results, to determine if ' +
                  'the persisted result apply to the current values')
    modifications = models.TextField(
        null=True,
        help_text='Serialized JSON representation of scenarios modifications ')
    modification_hash = models.CharField(
        max_length=255,
        null=True,
        help_text='A hash of the values for modifications to ' +
                  'compare to the existing model results, to determine if ' +
                  'the persisted result apply to the current values')
    aoi_census = models.TextField(
        null=True,
        help_text='Serialized JSON representation of AoI census ' +
                  'geoprocessing results')
    modification_censuses = models.TextField(
        null=True,
        help_text='Serialized JSON representation of modification censuses ' +
                  'geoprocessing results, with modification_hash')
    results = models.TextField(
        null=True,
        help_text='Serialized JSON representation of the model results')
    created_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=True)
    modified_at = models.DateTimeField(
        auto_now=True)

    def __unicode__(self):
        return self.name
