import factory
from pytest_factoryboy import named_model, register

from dependabot_alerts.core import Alert


@register
class AlertFactory(factory.Factory):
    """Factory for Alert objects."""

    class Meta:
        model = Alert
        exclude = ("organization", "repo")

    organization = factory.Sequence(lambda n: f"organization-{n}")
    repo = factory.Sequence(lambda n: f"repo-{n}")
    repo_full_name = factory.LazyAttribute(lambda o: f"{o.organization}/{o.repo}")
    ghsa_id = factory.Sequence(lambda n: f"GHSA-{n}")
    html_url = factory.LazyAttributeSequence(
        lambda o, n: f"https://github.com/{o.organization}/{o.repo}/security/dependabot/{n}"
    )
    package = factory.Sequence(lambda n: f"package-{n}")
    manifest_path = factory.Sequence(lambda n: f"manifest_path-{n}")
    summary = factory.Sequence(lambda n: f"summary-{n}")
    severity = factory.Faker("random_element", elements=["low", "medium", "high"])
    duplicates = []

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        if isinstance(kwargs["duplicates"], int):
            # Enable alert_factory(duplicates=n) to generate an Alert whose
            # Alert.duplicates attr is a list of n generated duplicate Alert's.
            kwargs["duplicates"] = cls.create_batch(
                size=kwargs["duplicates"],
                # Certain attributes would be expected to be the same for an
                # Alert's duplicates.
                organization=kwargs["organization"],
                repo=kwargs["repo"],
                ghsa_id=kwargs["ghsa_id"],
                package=kwargs["package"],
                summary=kwargs["summary"],
                severity=kwargs["severity"],
            )

        return kwargs


@register
class AlertDictFactory(AlertFactory):
    """Factory for alert dicts as returned by the GitHub API."""

    class Meta:
        model = named_model(dict, "AlertDict")

    @factory.post_generation
    def post(obj, *_args, **_kwargs):  # pylint:disable=no-self-argument
        """Transform the generated dict into the format returned by the GitHub API."""
        # pylint:disable=no-member
        repo_full_name = obj.pop("repo_full_name")
        ghsa_id = obj.pop("ghsa_id")
        package = obj.pop("package")
        manifest_path = obj.pop("manifest_path")
        summary = obj.pop("summary")
        severity = obj.pop("severity")
        del obj["duplicates"]

        # Serialise a dict in the format returned by the GitHub API.
        obj["repository"] = {"full_name": repo_full_name}
        obj["dependency"] = {
            "package": {
                "name": package,
            },
            "manifest_path": manifest_path,
        }
        obj["security_advisory"] = {
            "ghsa_id": ghsa_id,
            "summary": summary,
            "severity": severity,
        }
