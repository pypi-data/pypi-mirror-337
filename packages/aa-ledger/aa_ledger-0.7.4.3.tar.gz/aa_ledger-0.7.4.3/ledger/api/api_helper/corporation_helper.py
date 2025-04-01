import logging

from django.db.models import Q, Sum, QuerySet
from django.utils import timezone
from django.db.models.functions import TruncDay, TruncMonth, TruncHour
from dataclasses import dataclass
from typing import Any

from allianceauth.authentication.models import UserProfile

from ledger.api.api_helper.billboard_helper import ChartData
from ledger.models.corporationaudit import (
    CorporationAudit,
    CorporationWalletJournalEntry,
)

logger = logging.getLogger(__name__)


class CorporationProcess:
    """JournalProcess class to process the journal entries."""

    def __init__(self, corporation: CorporationAudit, date: timezone.datetime, view=None):
        self.corporation = corporation
        self.date = date
        self.view = view

    # pylint: disable=duplicate-code
    def _filter_date(self):
        """Filter the date."""
        filter_date = Q(date__year=self.date.year)
        if self.view == "month":
            filter_date &= Q(date__month=self.date.month)
        elif self.view == "day":
            filter_date &= Q(date__month=self.date.month)
            filter_date &= Q(date__day=self.date.day)
        return filter_date
    
    def wallet_check(self, types = None, first_party = None, second_party = None):
        """Get the wallet check for the corporation"""
        filter_date = self._filter_date()
        
        qs = (CorporationWalletJournalEntry.objects.filter(
                filter_date,
                division__corporation__corporation__corporation_id=self.corporation.corporation.corporation_id,
            )
        )
        
        if types:
            qs = qs.filter(ref_type__in=types)
        
        if first_party:
            qs = qs.filter(first_party__in=first_party)
        if second_party:
            qs = qs.filter(second_party__in=second_party)
        
        return qs
    
    def get_entity_ids(self):
        """Get the entity ids for the corporation"""
        filter_date = self._filter_date()
        qs = CorporationWalletJournalEntry.objects.filter(
            filter_date,
            division__corporation__corporation__corporation_id=self.corporation.corporation.corporation_id,
        )
        entity_ids_second = set(qs.values_list("second_party_id", flat=True))
        entity_ids_first = set(qs.values_list("first_party_id", flat=True))
        entity_ids = entity_ids_first | entity_ids_second
        return entity_ids
    
    def get_involved_alts(self, alts):
        """Get the involved alts for the corporation"""
        entity_ids = self.get_entity_ids()
        if not entity_ids:
            return set()
        return set(alts).intersection(entity_ids)
    
    def glance_bounty(self, second_party = None):
        """Get the glance bounty for the corporation"""
        types = ["bounty_prizes"]
        return self.wallet_check(
            types=types, second_party=second_party
        ).aggregate(total=Sum("amount"))["total"] or 0
        
    def glance_ess(self, second_party = None):
        """Get the glance ess for the corporation"""
        types = ["ess_escrow_transfer"]
        return self.wallet_check(
            types=types, second_party=second_party
        ).aggregate(total=Sum("amount"))["total"] or 0
        
    def glance_industry_tax(self, first_party = None):
        """Get the glance industry for the corporation"""
        types = ["industry_job_tax", "reprocessing_tax"]
        return self.wallet_check(
            types=types, first_party=first_party
        ).aggregate(total=Sum("amount"))["total"] or 0
        
    def glance_daily_goal(self, second_party = None):
        """Get the glance daily goal for the corporation"""
        types = ["daily_goal_payouts"]
        return self.wallet_check(
            types=types, second_party=second_party
        ).aggregate(total=Sum("amount"))["total"] or 0
        
    def glance_mission(self, second_party = None):
        """Get the glance mission for the corporation"""
        types = ["agent_mission_reward", "agent_mission_time_bonus_reward"]
        return self.wallet_check(
            types=types, second_party=second_party
        ).aggregate(total=Sum("amount"))["total"] or 0
        
    def glance_incursion(self, second_party = None):
        """Get the glance incursion for the corporation"""
        types = ["corporate_reward_payout"]
        return self.wallet_check(
            types=types, second_party=second_party
        ).aggregate(total=Sum("amount"))["total"] or 0
    
    
    def generate_ledger_new(self):
        accounts = UserProfile.objects.filter(
            main_character__isnull=False,
        ).select_related(
            "user__profile__main_character",
            "main_character__character_ownership",
            "main_character__character_ownership__user__profile",
            "main_character__character_ownership__user__profile__main_character",
        )
        
        main_dict = {}
        billoard = BillboardSystem(view=self.view, journal=self.wallet_check(), corporation=self.corporation)
        
        accounts_bounty = 0
        accounts_ess = 0
        accounts_miscellaneous = 0
        
        for account in accounts:
            alts = account.user.character_ownerships.all().values_list(
                "character__character_id", flat=True
            )
            alts = self.get_involved_alts(alts)
            
            if not alts:
                continue
            
            bounty = self.glance_bounty(alts)
            ess = self.glance_ess(alts)
            industry_tax = self.glance_industry_tax(alts)
            daily_goal = self.glance_daily_goal(alts)
            mission = self.glance_mission(alts)
            incursion = self.glance_incursion(alts)
            
            miscellaneous = industry_tax + daily_goal + mission + incursion
            
            data = {
                "main_id": account.user.profile.main_character.character_id,
                "main_name": account.user.profile.main_character.character_name,
                "entity_type": "character",
                "alt_names": list(alts),
                "total_amount": bounty,
                "total_amount_ess": ess,
                "total_amount_others": miscellaneous,
            } 
            main_dict[account.user.profile.main_character.character_id] = data
            
            accounts_bounty += bounty
            accounts_ess += ess
            accounts_miscellaneous += miscellaneous
            billoard.chord_add_data(data)
            
        
        total_miscellaneous = self.glance_industry_tax() + self.glance_daily_goal() + self.glance_mission() + self.glance_incursion()
        total_bounty = self.glance_bounty()
        total_ess = self.glance_ess()
        
        other_bounty = total_bounty - accounts_bounty
        other_ess = total_ess - accounts_ess
        
        data = {
            "main_id": self.corporation.corporation.corporation_id,
            "main_name": self.corporation.corporation.corporation_name,
            "entity_type": "corporation",
            "alt_names": [],
            "total_amount": other_bounty,
            "total_amount_ess": other_ess,
            "total_amount_others": total_miscellaneous - accounts_miscellaneous,
        }
        
        main_dict[self.corporation.corporation.corporation_id] = data
        billoard.chord_add_data(data)
           
        output = {
            "ratting": sorted(
                list(main_dict.values()), key=lambda x: x["main_name"]
            ),
            "billboard": {
                "standard": {
                    "charts": billoard.chord,
                    "rattingbar": billoard.rattingbar,
                    "workflow": None,
                },
            },
            "total": {
                "total_amount": total_bounty,
                "total_amount_ess": total_ess,
                "total_amount_others": total_miscellaneous,
                "total_amount_all": total_bounty + total_ess + total_miscellaneous,
            },
        }

        return output
    
@dataclass
class ChartData:
    title: str
    categories: list[str]
    series: list[dict[str, Any]]
    
class BillboardSystem:
    """BillboardSystem class to process billboard data."""
    def __init__(self, view, journal: QuerySet[CorporationWalletJournalEntry], corporation: CorporationAudit):
        self.view = view
        self.journal = journal
        self.corporation = corporation
        
        self.chord = ChartData(title="Chords", categories=[], series=[])
        self.rattingbar = ChartData(title="Ratting Bar", categories=["Bounty", "ESS", "Miscellaneous"], series=self._ratting_data())
        self.workflow = ChartData(title="Workflow", categories=[], series=[])
        
    def chord_add_data(self, data: dict):
        """Add chord data"""
        self.chord.series.append(
            {
                "from": data["main_name"],
                "to": self.corporation.corporation.corporation_name,
                "value": data["total_amount"] + data["total_amount_ess"] + data["total_amount_others"],
                "main": data["main_name"],
            }
        )
        return self.chord
    
    def _ratting_bar(self, results: dict):
        """Get the ratting bar for the corporation"""
        formatted_results = []
        for date, values in results.items():
            formatted_results.append({
                "date": date.strftime("%Y-%m-%d"),
                "bounty": int(values.get("bounty", 0)),
                "ess": int(values.get("ess", 0)),
                "miscellaneous": int(values.get("miscellaneous", 0)),
            })
        return formatted_results
    
    def _ratting_data(self):
        """Create the ratting data for the billboard"""
        types = [
            "bounty_prizes", 
            "ess_escrow_transfer", 
            "industry_job_tax", 
            "reprocessing_tax", 
            "daily_goal_payouts", 
            "agent_mission_reward", 
            "agent_mission_time_bonus_reward"
        ]
        qs = self.journal.filter(ref_type__in=types)
        
        if self.view == "year":
            qs = qs.annotate(period=TruncMonth("date"))
        elif self.view == "month":
            qs = qs.annotate(period=TruncDay("date"))
        elif self.view == "day":
            qs = qs.annotate(period=TruncHour("date"))
        else:
            raise ValueError("Invalid view type. Use 'day', 'month', or 'year'.")
        
        # Aggregate data by day and ref_type
        qs = qs.values("period", "ref_type").annotate(total_amount=Sum("amount"))

        result = {}
        
        for entry in qs:
            period = entry["period"]
            ref_type = entry["ref_type"]
            total_amount = entry["total_amount"]

            if period not in result:
                result[period] = {"bounty": 0, "ess": 0, "miscellaneous": 0}

            if ref_type == "bounty_prizes":
                result[period]["bounty"] += total_amount
            elif ref_type == "ess_escrow_transfer":
                result[period]["ess"] += total_amount
            else:
                result[period]["miscellaneous"] += total_amount
        return self._ratting_bar(result)
        
        
        