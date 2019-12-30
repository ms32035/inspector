from model_utils import Choices

SUBMIT_CSS_CLASSES = "primaryAction btn btn-primary btn-block btn-sm"
STATUSES = Choices(
    ("NEW", "New"), ("RUNNING", "Running"), ("FINISHED", "Finished"), ("ERROR", "Error")
)
ICONS = {
    "environment": '<i class="fas fa-globe-africa" title="Environment"></i>',
    "datacheck": '<i class="fas fa-list" title="Check code"></i>',
    "status": '<i class="far fa-clock" title="Status"></i>',
    "table": '<i class="fas fa-table" title="Table"></i>',
    "schema": '<i class="fas fa-object-group" title="Schema"></i>',
    "system": '<i class="fas fa-desktop" title="System"></i>',
    "result": '<i class="fas fa-question" title="Result"></i>',
    "user": '<i class="fas fa-user-cog" title="User"></i>',
    "start": '<i class="far fa-square" title="Start"></i> <i class="fas fa-angle-double-right"></i>',
    "end": '<i class="fas fa-angle-double-right"></i> <i class="fas fa-square" title="End"></i>',
    "report": '<i class="fas fa-file-alt" title="Report"></i>',
    "host": '<i class="fas fa-network-wired" title="Host"></i>',
    "application": '<i class="far fa-window-maximize" title="Application"></i>',
    "last_run": '<i class="far fa-clock" title="Last run"></i>',
}

STATUS_ICONS = {
    "NEW": "",
    "ERROR": '<i class="fas fa-exclamation" title="Error" style="color:red"></i>',
    "FINISHED": '<i class="fas fa-square" title="Finished"></i>',
    "RUNNING": '<i class="far fa-square" title="Running"></i>',
}

RESULT_ICONS = {
    None: "",
    "FAILED": '<i class="fas fa-times" style="color:red"></i>',
    "SUCCESS": '<i class="fas fa-check" style="color:green"></i>',
    "WARNING": '<i class="fas fa-exclamation-triangle" style="color:yellow"></i>',
}
