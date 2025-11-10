"""
Approval Workflow Module
Manages the approval workflow for property analyses
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Approval status states"""
    PENDING = "pending"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISIONS_NEEDED = "revisions_needed"


class ApprovalWorkflow:
    """Manages approval workflow for analyses"""

    def __init__(self):
        """Initialize approval workflow"""
        self.approvals: Dict[str, Dict[str, Any]] = {}
        logger.info("Approval Workflow initialized")

    def create_approval_request(
        self,
        analysis_id: str,
        property_address: str,
        analysis: Dict[str, Any],
        requested_by: str = "System"
    ) -> Dict[str, Any]:
        """
        Create a new approval request

        Args:
            analysis_id: Unique analysis ID
            property_address: Property address
            analysis: Analysis to be approved
            requested_by: Who requested the approval

        Returns:
            Approval request record
        """
        approval_request = {
            "analysis_id": analysis_id,
            "property_address": property_address,
            "status": ApprovalStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "requested_by": requested_by,
            "reviewed_by": None,
            "reviewed_at": None,
            "approval_notes": "",
            "estimated_value": analysis.get("valuation", {}).get("estimated_value", 0),
            "investment_score": analysis.get("investment_analysis", {}).get("investment_score", 0),
            "roi_percentage": analysis.get("investment_analysis", {}).get("roi_percentage", 0),
            "revision_count": 0,
            "approval_history": []
        }

        self.approvals[analysis_id] = approval_request
        logger.info(f"Approval request created for {analysis_id}")

        return approval_request

    def submit_for_review(
        self,
        analysis_id: str,
        reviewer_name: str
    ) -> Dict[str, Any]:
        """
        Submit analysis for review

        Args:
            analysis_id: Analysis ID to review
            reviewer_name: Name of reviewer

        Returns:
            Updated approval record
        """
        if analysis_id not in self.approvals:
            return {"error": f"Analysis {analysis_id} not found"}

        approval = self.approvals[analysis_id]
        approval["status"] = ApprovalStatus.REVIEWING.value
        approval["reviewed_by"] = reviewer_name
        approval["reviewed_at"] = datetime.now().isoformat()

        approval["approval_history"].append({
            "action": "submitted_for_review",
            "by": reviewer_name,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"Analysis {analysis_id} submitted for review by {reviewer_name}")
        return approval

    def approve_analysis(
        self,
        analysis_id: str,
        reviewer_name: str,
        approval_notes: str = ""
    ) -> Dict[str, Any]:
        """
        Approve an analysis

        Args:
            analysis_id: Analysis to approve
            reviewer_name: Name of approver
            approval_notes: Optional approval notes

        Returns:
            Updated approval record
        """
        if analysis_id not in self.approvals:
            return {"error": f"Analysis {analysis_id} not found"}

        approval = self.approvals[analysis_id]
        approval["status"] = ApprovalStatus.APPROVED.value
        approval["reviewed_by"] = reviewer_name
        approval["reviewed_at"] = datetime.now().isoformat()
        approval["approval_notes"] = approval_notes

        approval["approval_history"].append({
            "action": "approved",
            "by": reviewer_name,
            "notes": approval_notes,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"Analysis {analysis_id} approved by {reviewer_name}")
        return approval

    def reject_analysis(
        self,
        analysis_id: str,
        reviewer_name: str,
        rejection_reason: str
    ) -> Dict[str, Any]:
        """
        Reject an analysis

        Args:
            analysis_id: Analysis to reject
            reviewer_name: Name of reviewer rejecting
            rejection_reason: Reason for rejection

        Returns:
            Updated approval record
        """
        if analysis_id not in self.approvals:
            return {"error": f"Analysis {analysis_id} not found"}

        approval = self.approvals[analysis_id]
        approval["status"] = ApprovalStatus.REJECTED.value
        approval["reviewed_by"] = reviewer_name
        approval["reviewed_at"] = datetime.now().isoformat()
        approval["approval_notes"] = rejection_reason

        approval["approval_history"].append({
            "action": "rejected",
            "by": reviewer_name,
            "reason": rejection_reason,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"Analysis {analysis_id} rejected by {reviewer_name}: {rejection_reason}")
        return approval

    def request_revisions(
        self,
        analysis_id: str,
        reviewer_name: str,
        revision_notes: str
    ) -> Dict[str, Any]:
        """
        Request revisions for an analysis

        Args:
            analysis_id: Analysis needing revisions
            reviewer_name: Name of reviewer
            revision_notes: Details of revisions needed

        Returns:
            Updated approval record
        """
        if analysis_id not in self.approvals:
            return {"error": f"Analysis {analysis_id} not found"}

        approval = self.approvals[analysis_id]
        approval["status"] = ApprovalStatus.REVISIONS_NEEDED.value
        approval["reviewed_by"] = reviewer_name
        approval["reviewed_at"] = datetime.now().isoformat()
        approval["approval_notes"] = revision_notes
        approval["revision_count"] = approval.get("revision_count", 0) + 1

        approval["approval_history"].append({
            "action": "revisions_requested",
            "by": reviewer_name,
            "notes": revision_notes,
            "revision_count": approval["revision_count"],
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"Revisions requested for {analysis_id} by {reviewer_name}")
        return approval

    def get_approval_status(self, analysis_id: str) -> Dict[str, Any]:
        """
        Get approval status for an analysis

        Args:
            analysis_id: Analysis ID to check

        Returns:
            Approval status information
        """
        if analysis_id not in self.approvals:
            return {"error": f"Analysis {analysis_id} not found"}

        return self.approvals[analysis_id]

    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """
        Get all pending approvals

        Returns:
            List of pending approval requests
        """
        return [
            approval for approval in self.approvals.values()
            if approval["status"] == ApprovalStatus.PENDING.value
        ]

    def get_approval_statistics(self) -> Dict[str, Any]:
        """
        Get approval workflow statistics

        Returns:
            Statistics about approvals
        """
        total = len(self.approvals)
        by_status = {}

        for approval in self.approvals.values():
            status = approval["status"]
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "total_approvals": total,
            "by_status": by_status,
            "pending_count": by_status.get(ApprovalStatus.PENDING.value, 0),
            "approved_count": by_status.get(ApprovalStatus.APPROVED.value, 0),
            "rejected_count": by_status.get(ApprovalStatus.REJECTED.value, 0),
            "revisions_needed_count": by_status.get(ApprovalStatus.REVISIONS_NEEDED.value, 0)
        }

    def clear_approvals(self) -> None:
        """Clear all approval records"""
        self.approvals.clear()
        logger.info("All approval records cleared")
