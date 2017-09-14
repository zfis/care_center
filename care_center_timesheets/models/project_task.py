# -*- coding: utf-8 -*-
from odoo import models, api


class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = ['project.utils', 'project.task']

    def _update_timesheets(self):
        """
        If the Task Project or Partner changes, then
        we must update the Timesheets as well.
        """
        aa = self.project_id.analytic_account_id
        team = self.project_id.team_id

        data = {
            'project_id': self.project_id.id,
            'partner_id': self.partner_id.id,
            'analytic_account_id': aa and aa.id,
            'team_id': team and team.id,
        }

        for ts in self.timesheet_ids:
            ts.write(data)

    @api.multi
    def write(self, vals):
        issue = super(ProjectTask, self).write(vals)

        if vals.get('partner_id') or vals.get('project_id'):
            self._update_timesheets()

        return issue
