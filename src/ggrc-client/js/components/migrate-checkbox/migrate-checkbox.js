/*
    Copyright (C) 2020 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
import canComponent from 'can-component';
import canMap from 'can-map';
import template from './migrate-checkbox.stache';
import {isAllowedFor} from '../../permission';
import {notifierXHR, notifier} from '../../plugins/utils/notifiers-utils';
import {isConnectionLost} from '../../plugins/utils/errors-utils';
import {isSnapshot} from '../../plugins/utils/snapshot-utils';

const MIGRATE_OBJECTS = ['Contract', 'DataAsset', 'Facility', 'Market',
  'Metric', 'Objective', 'OrgGroup', 'Policy', 'Process', 'Product',
  'ProductGroup', 'Project', 'Regulation', 'Requirement', 'Standard',
  'System', 'TechnologyEnvironment', 'Threat', 'Vendor'];

export default canComponent.extend({
  tag: 'migrate-checkbox',
  view: canStache(template),
  leakScope: true,
  viewModel: canMap.extend({
    define: {
      isMigrateObject: {
        get() {
          const instance = this.instance;
          return MIGRATE_OBJECTS.includes(instance.type)
            && !isSnapshot(instance);
        },
      },
      disabled: {
        get() {
          const readOnly = this.attr('instance.readonly');
          const canEdit = isAllowedFor('update', this.attr('instance'));
          if (!readOnly && canEdit) {
            return this.attr('isSaving');
          }
          return true;
        },
      },
    },
    isSaving: false,
    isEditModal: false,
    instance: null,
    saveInstance() {
      this.attr('isSaving', true);
      return this.attr('instance')
        .save().then(() => {
          $(document.body).trigger('ajax:flash', {
            success: 'Saved',
          });
        }).catch((instance, xhr) => {
          if (isConnectionLost()) {
            notifier('error', 'Internet connection was lost');
          } else {
            notifierXHR('error', xhr);
          }
        }).always(() => {
          this.attr('isSaving', false);
        });
    },
  }),
});
