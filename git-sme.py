import click
from collections import Counter
import git
import nltk

__author__ = "Chris Altonji"

@click.group()
def main():
    """
    A CLI for finding subjects and subject matter experts in a git repo.
    """
    pass

@main.command()
@click.option('--repo', required=True)
@click.option('--branch', default="master")
@click.option('--language', default="english")
def subjects(repo, branch, language):
    """Find subjects within a repo"""
    repo = git.Repo(repo)
    commits = list(repo.iter_commits(branch))
    print(f"commit length: {len(commits)}")
    messages = [commit.message for commit in commits]
    messages_str = ("\n\n".join(messages)).lower()

    nltk.download("stopwords")
    stoplist = set(nltk.corpus.stopwords.words(language))

    ngrams = nltk.ngrams(messages_str.split(), 2)
    cleangrams = [gram for gram in ngrams if not any(stop in gram for stop in stoplist)]
    ngram_counts = Counter(cleangrams)

    print(ngram_counts.most_common(40))

@main.command()
@click.option('--repo', required=True)
@click.option('--branch', default="master")
@click.option('--subject', required=True)
def experts(repo, branch, subject):
    """Find experts of a given subject within a repo"""
    repo = git.Repo(repo)
    commits = list(repo.iter_commits(branch))

    subject = subject.lower()
    subject_no_space = "".join(subject.split())
    user_counts = Counter()
    for commit in commits:
        message = commit.message.lower()
        if subject in message or subject_no_space in message:
            user_counts[commit.author] += 1
    for value, count in user_counts.most_common():
        print(f"{value}, {count}")


if __name__ == "__main__":
    main()