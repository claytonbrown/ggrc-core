/*
    Copyright (C) 2020 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canMap from 'can-map';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../migrate-checkbox';
import * as NotifiersUtils from '../../../plugins/utils/notifiers-utils';
import * as ErrorsUtils from '../../../plugins/utils/errors-utils';

describe('migrate-checkbox component', () => {
  let viewModel;
  let instance;
  let dfdSave;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
    dfdSave = $.Deferred();
    instance = new canMap({
      save: jasmine.createSpy().and.returnValue(dfdSave),
    });

    viewModel.attr('instance', instance);
  });

  describe('saveInstance() method', () => {
    it('sets true to isSaving attribute', () => {
      viewModel.attr('isSaving', false);

      viewModel.saveInstance();

      expect(viewModel.attr('isSaving')).toBe(true);
    });

    it('calls instance\'s save() method', () => {
      viewModel.saveInstance();

      expect(instance.save).toHaveBeenCalled();
    });

    describe('after instance.save() success', () => {
      beforeEach(() => {
        dfdSave.resolve();
        spyOn($.fn, 'trigger').and.callThrough();
      });

      it('was notified when was saved successfully', async () => {
        await viewModel.saveInstance();

        expect($.fn.trigger).toHaveBeenCalledWith('ajax:flash', {
          success: ['Saved'],
        });
      });

      it('sets false to isSaving attribute', async () => {
        viewModel.attr('isSaving', true);

        await viewModel.saveInstance();

        expect(viewModel.attr('isSaving')).toBe(false);
      });
    });

    describe('after instance.save() was failed', () => {
      beforeEach(() => {
        dfdSave.reject({}, 'fakeXhr');
        spyOn(NotifiersUtils, 'notifier');
        spyOn(NotifiersUtils, 'notifierXHR');
        spyOn(ErrorsUtils, 'isConnectionLost')
          .and.returnValue(false);
      });

      it('calls notifier() util if internet connection was lost',
        async () => {
          ErrorsUtils.isConnectionLost.and.returnValue(true);

          await viewModel.saveInstance();

          expect(NotifiersUtils.notifier).toHaveBeenCalledWith(
            'error', 'Internet connection was lost');
        });

      it('calls notifierXHR() by default', async () => {
        await viewModel.saveInstance();

        expect(NotifiersUtils.notifierXHR).toHaveBeenCalledWith(
          'error', 'fakeXhr');
      });

      it('sets false to isSaving attribute', async () => {
        viewModel.attr('isSaving', true);

        await viewModel.saveInstance();

        expect(viewModel.attr('isSaving')).toBe(false);
      });
    });
  });
});
