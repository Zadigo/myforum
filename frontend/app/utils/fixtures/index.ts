import { faker } from '@faker-js/faker'
import type { Forums, MainThreads, UserComments, ThreadPoll, LatestComments, SingleForum, SingleMainThread } from '~/types'

export const pollFixture: ThreadPoll = {
  data: {
    threadPoll: {
      id: faker.number.int().toString(),
      pollType: 'single-choice',
      public: true,
      question: faker.lorem.sentence(),
      votersAlone: false,
      active: true,
      possibilitySet: [
        {
          id: faker.number.int().toString(),
          createdOn: faker.date.past().toISOString(),
          text: faker.lorem.words(2)
        },
        {
          id: faker.number.int().toString(),
          createdOn: faker.date.past().toISOString(),
          text: faker.lorem.words(2)
        }
      ],
      createdOn: faker.date.past().toISOString(),
      closingDate: faker.date.future().toISOString(),
      choicesLimit: 1,
      closes: false,
      allowVoteChange: true,
      answerSet: []
    }
  }
}

export const mainThreadsFixture: MainThreads = {
  data: {
    allMainThreads: {
      edges: [
        {
          node: {
            id: faker.number.int().toString(),
            title: faker.lorem.words(5),
            user: {
              id: faker.number.int().toString(),
              username: faker.person.firstName()
            },
            forum: {
              id: faker.number.int().toString(),
              title: faker.lorem.words(3)
            },
            category: faker.lorem.word(),
            numberOfComments: faker.number.int({ min: 0, max: 500 }),
            ownedByUser: false,
            pinned: false,
            highlighted: false,
            published: true,
            active: true,
            modifiedOn: faker.date.recent().toISOString(),
            createdOn: faker.date.past().toISOString()
          }
        }
      ]
    }
  }
}

export const mainThreadFixture: SingleMainThread= {
  data: {
    mainThread: {
      id: faker.number.int().toString(),
      title: faker.lorem.words(5),
      user: {
        id: faker.number.int().toString(),
        username: faker.person.firstName()
      },
      forum: {
        id: faker.number.int().toString(),
        title: faker.lorem.words(3)
      },
      category: faker.lorem.word(),
      numberOfComments: faker.number.int({ min: 0, max: 500 }),
      ownedByUser: false,
      pinned: false,
      highlighted: false,
      published: true,
      active: true,
      modifiedOn: faker.date.recent().toISOString(),
      createdOn: faker.date.past().toISOString()
    }
  }
}

export const forumsFixture: Forums = {
  data: {
    allForums: {
      edges: [
        {
          node: {
            id: faker.number.int().toString(),
            title: faker.lorem.words(3),
            description: faker.lorem.sentence(),
            category: faker.lorem.word(),
            active: true,
            numberOfThreads: faker.number.int({ min: 0, max: 100 }),
            user: {
              id: faker.number.int().toString(),
              username: faker.person.firstName()
            },
            createdOn: faker.date.past().toISOString()
          }
        }
      ]
    }
  }
}

export const forumFixture: SingleForum= {
  data: {
    forum: {
      id: faker.number.int().toString(),
      title: faker.lorem.words(3),
      description: faker.lorem.sentence(),
      category: faker.lorem.word(),
      active: true,
      numberOfThreads: faker.number.int({ min: 0, max: 100 }),
      user: {
        id: faker.number.int().toString(),
        username: faker.person.firstName()
      },
      createdOn: faker.date.past().toISOString()
    }
  }
}

export const commentsFixture: UserComments = {
  data: {
    commentsForThread: {
      edges: Array.from({ length: 3 }).map(() => ({
        node: {
          id: faker.number.int().toString(),
          active: true,
          content: faker.lorem.paragraphs(2),
          contentDelta: null,
          contentHtml: `<p>${faker.lorem.paragraphs(2)}</p>`,
          originalPost: false,
          pinned: false,
          published: true,
          title: null,
          quoteSet: [],
          quotedOmment: [],
          replySet: [],
          mediaContents: [],
          bookmarkedByUser: faker.datatype.boolean(),
          user: {
            id: faker.number.int().toString(),
            username: faker.person.firstName()
          },
          createdOn: faker.date.past().toISOString(),
          modifiedOn: faker.date.recent().toISOString()
        }
      }))
    }
  }
}

export const latestCommentsFixture: LatestComments = {
  data: {
    latestComments: {
      edges: Array.from({ length: 5 }).map(() => ({
        node: {
          id: faker.number.int().toString(),
          title: faker.lorem.sentence(),
          content: faker.lorem.paragraph(),
          contentHtml: `<p>${faker.lorem.paragraph()}</p>`,
          createdOn: faker.date.recent().toISOString(),
          user: {
            id: faker.number.int().toString(),
            username: faker.person.firstName()
          }
        }
      }))
    }
  }
}

