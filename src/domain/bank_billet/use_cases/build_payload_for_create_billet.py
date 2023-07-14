import logging
from dataclasses import dataclass
from datetime import date

from babel.numbers import format_decimal

from src.common.helpers import DateHelper
from src.infra.adapters.database.orm import FinancialInstallment, Financing

logger = logging.getLogger(__name__)


@dataclass
class BuildPayload:
    financial_installments: FinancialInstallment
    financings: Financing

    async def build_payload_for_create_billet(self) -> dict:
        try:
            return self._build_struct_to_send()
        except Exception as err:
            logger.warning(f'Error when trying create payload, error: {err}')  # noqa G004
            raise err

    def description(self):
        payment_slip_number = self.financial_installments.number
        payment_slip_number_total = self.financings.installments_number
        return f'Parcela Nº {payment_slip_number}/{payment_slip_number_total} do Financiamento Solfácil'

    @staticmethod
    def _instructions_default():
        return """Você também consegue acessar seus boletos através do nosso portal: cliente.xpto.com.br
        Guarde esse site, para consultar quando precisar."""

    def _put_additional_numbers(self):
        value = str(self.financial_installments.number)
        number = value.rjust(3, '0')
        return f'{self.financial_installments.financing_id}{number}'

    def _tags(self):
        type_billet = 'regular'
        date_billet = self.parse_date()
        currency = format_decimal(self.financial_installments.amount, format='#,##0.00', locale='pt_BR')
        return [
            type_billet,
            date_billet,
            f'{self.financial_installments.number}[{currency}/' f'{self.financings.identifier}/{type_billet}]',
        ]

    def parse_date(self):
        month_short, year = date.strftime(self.financial_installments.expire_on, '%b-%y').split('-')
        translated_month_short = DateHelper.translate_month(month_short)
        return f'{translated_month_short}-{year}'

    def _build_struct_to_send(self):
        return {
            'amount': self.financial_installments.amount,
            'expireAt': self.financial_installments.expire_on.strftime('%Y-%m-%d'),
            'description': self.description(),
            'instructions': self._instructions_default(),
            'documentNumber': self._put_additional_numbers(),
            'controlNumber': self._put_additional_numbers(),
            'tags': self._tags(),
            'customerID': self.financings.customer_id,
            'fineType': 1,
            'finePercentage': '2.00',
            'fineValue': '0.01',
            'daysForFine': 1,
            'interestType': 0,
            'interestPercentage': '0.03',
            'interestValue': '0.01',
            'daysToInterest': 1,
        }
